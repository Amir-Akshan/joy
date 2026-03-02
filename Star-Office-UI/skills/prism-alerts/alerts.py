#!/usr/bin/env python3
"""
Pump.fun Alert Bot - PRISM API Integration
Real-time alerts for Solana token launches, graduations, and volume spikes
"""

import os
import sys
import json
import time
import sqlite3
import asyncio
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
from dataclasses import dataclass, asdict
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

@dataclass
class Token:
    """Represents a Pump.fun token"""
    token_id: str
    symbol: str
    name: str
    market_cap: float
    holders: int
    bonding_progress: float
    created_at: str
    url: str
    status: str = "bonding"

class PrismClient:
    """PRISM API Client for accessing Pump.fun data"""
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or os.getenv('PRISM_URL', 'https://strykr-prism.up.railway.app')
        self.session = requests.Session()
        self.session.timeout = 10
    
    def get_bonding_tokens(self, limit: int = 50) -> List[Token]:
        """Get tokens currently on bonding curve"""
        try:
            url = f"{self.base_url}/crypto/trending/solana/bonding"
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            tokens = []
            
            # API returns 'tokens' not 'data'
            token_list = data.get('tokens', [])[:limit]
            
            for item in token_list:
                # Use fully_diluted_valuation as market cap
                market_cap = float(item.get('fully_diluted_valuation', 0))
                
                # Skip tokens under $100 market cap
                if market_cap < 100:
                    continue
                
                token = Token(
                    token_id=item.get('address', ''),
                    symbol=item.get('symbol', 'UNKNOWN'),
                    name=item.get('name', ''),
                    market_cap=market_cap,
                    holders=1,  # API doesn't provide holders count
                    bonding_progress=float(item.get('bonding_curve_progress', 0) or 0),
                    created_at=item.get('updated_at', ''),
                    url=f"https://pump.fun/{item.get('address', '')}",
                    status='bonding'
                )
                tokens.append(token)
            
            logger.info(f"Fetched {len(tokens)} bonding tokens from {len(token_list)} total")
            return tokens
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching bonding tokens: {e}")
            return []
    
    def get_graduated_tokens(self, limit: int = 50) -> List[Token]:
        """Get tokens that graduated from bonding curve"""
        try:
            url = f"{self.base_url}/crypto/trending/solana/graduated"
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            tokens = []
            
            # API returns 'tokens' not 'data'
            token_list = data.get('tokens', [])[:limit]
            
            for item in token_list:
                # Use fully_diluted_valuation as market cap
                market_cap = float(item.get('fully_diluted_valuation') or 0)
                
                token = Token(
                    token_id=item.get('address', ''),
                    symbol=item.get('symbol', 'UNKNOWN'),
                    name=item.get('name', ''),
                    market_cap=market_cap,
                    holders=1,  # API doesn't provide holders count
                    bonding_progress=100.0,  # Graduated = 100%
                    created_at=item.get('updated_at', ''),
                    url=f"https://pump.fun/{item.get('address', '')}",
                    status='graduated'
                )
                tokens.append(token)
            
            logger.info(f"Fetched {len(tokens)} graduated tokens from {len(token_list)} total")
            return tokens
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching graduated tokens: {e}")
            return []

class AlertDatabase:
    """SQLite database for alert deduplication"""
    
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or 'alerts.db'
        self._init_db()
    
    def _init_db(self):
        """Initialize database tables"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    token_id TEXT NOT NULL,
                    alert_type TEXT NOT NULL,
                    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(token_id, alert_type)
                )
            ''')
            conn.commit()
    
    def has_alert(self, token_id: str, alert_type: str, cooldown_minutes: int = 5) -> bool:
        """Check if alert was recently sent"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT sent_at FROM alerts 
                WHERE token_id = ? AND alert_type = ?
                ORDER BY sent_at DESC LIMIT 1
            ''', (token_id, alert_type))
            
            row = cursor.fetchone()
            if not row:
                return False
            
            sent_time = datetime.fromisoformat(row[0])
            cooldown = datetime.now() - timedelta(minutes=cooldown_minutes)
            
            return sent_time > cooldown
    
    def record_alert(self, token_id: str, alert_type: str):
        """Record that an alert was sent"""
        with sqlite3.connect(self.db_path) as conn:
            try:
                conn.execute('''
                    INSERT INTO alerts (token_id, alert_type)
                    VALUES (?, ?)
                ''', (token_id, alert_type))
                conn.commit()
            except sqlite3.IntegrityError:
                # Update existing record
                conn.execute('''
                    UPDATE alerts SET sent_at = CURRENT_TIMESTAMP
                    WHERE token_id = ? AND alert_type = ?
                ''', (token_id, alert_type))
                conn.commit()

class AlertManager:
    """Manages alert formatting and distribution"""
    
    def __init__(self):
        self.db = AlertDatabase()
        self.enable_telegram = os.getenv('ENABLE_TELEGRAM', 'false').lower() == 'true'
        self.enable_discord = os.getenv('ENABLE_DISCORD', 'false').lower() == 'true'
        self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_channel = os.getenv('TELEGRAM_CHANNEL_ID')
        self.discord_token = os.getenv('DISCORD_BOT_TOKEN')
        self.discord_channel = os.getenv('DISCORD_CHANNEL_ID')
    
    def format_new_launch_alert(self, token: Token) -> str:
        """Format new token launch alert"""
        return f"""🚀 NEW PUMP.FUN TOKEN

${token.symbol}
{token.name}
CA: {token.token_id}

📊 Stats:
• Bonding Progress: {token.bonding_progress:.1f}%
• Market Cap: ${token.market_cap:,.0f}
• Holders: {token.holders}
• Created: {token.created_at}

🔗 {token.url}"""
    
    def format_graduation_alert(self, token: Token) -> str:
        """Format token graduation alert"""
        return f"""🎓 TOKEN GRADUATED!

${token.symbol} ({token.name}) just graduated to DEX!

📊 Final Stats:
• Market Cap: ${token.market_cap:,.0f}
• Total Holders: {token.holders}
• Graduation Time: {token.created_at}

Trading now live!
🔗 {token.url}"""
    
    def format_volume_spike_alert(self, token: Token, volume_increase: float) -> str:
        """Format volume spike alert"""
        return f"""📈 VOLUME SPIKE DETECTED

${token.symbol} seeing unusual activity

• Volume Increase: +{volume_increase:.0f}%
• Market Cap: ${token.market_cap:,.0f}
• Holders: {token.holders}

⚠️ Could be coordinated buy - DYOR
🔗 {token.url}"""
    
    def send_telegram_alert(self, message: str) -> bool:
        """Send alert via Telegram"""
        if not self.enable_telegram or not self.telegram_token or not self.telegram_channel:
            return False
        
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            payload = {
                'chat_id': self.telegram_channel,
                'text': message,
                'parse_mode': 'HTML'
            }
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info("Telegram alert sent successfully")
            return True
        except Exception as e:
            logger.error(f"Error sending Telegram alert: {e}")
            return False
    
    def send_discord_alert(self, message: str) -> bool:
        """Send alert via Discord"""
        if not self.enable_discord or not self.discord_token or not self.discord_channel:
            return False
        
        try:
            url = f"https://discordapp.com/api/channels/{self.discord_channel}/messages"
            headers = {'Authorization': f'Bot {self.discord_token}'}
            payload = {'content': message}
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            logger.info("Discord alert sent successfully")
            return True
        except Exception as e:
            logger.error(f"Error sending Discord alert: {e}")
            return False
    
    def send_alert(self, message: str, token: Token, alert_type: str = 'generic'):
        """Send alert through all configured channels"""
        
        # Check cooldown
        if self.db.has_alert(token.token_id, alert_type):
            logger.debug(f"Alert for {token.symbol} ({alert_type}) in cooldown, skipping")
            return
        
        # Send through configured channels
        self.send_telegram_alert(message)
        self.send_discord_alert(message)
        print(message)
        
        # Record alert
        self.db.record_alert(token.token_id, alert_type)

class TokenFilter:
    """Filter tokens based on configured criteria"""
    
    def __init__(self):
        self.min_market_cap = float(os.getenv('MIN_MARKET_CAP', 5000))
        self.max_market_cap = float(os.getenv('MAX_MARKET_CAP', 100000))
        self.min_holders = int(os.getenv('MIN_HOLDERS', 10))
        self.bonding_threshold = float(os.getenv('BONDING_PROGRESS_THRESHOLD', 20))
    
    def should_alert(self, token: Token, token_type: str = 'bonding') -> bool:
        """Check if token meets alert criteria"""
        
        # Market cap filters
        if token.market_cap < self.min_market_cap or token.market_cap > self.max_market_cap:
            return False
        
        # Holder filters
        if token.holders < self.min_holders:
            return False
        
        # Bonding progress filter for new tokens
        if token_type == 'bonding' and token.bonding_progress < self.bonding_threshold:
            return False
        
        return True

class StateManager:
    """Manages Star Office UI state.json file"""
    
    def __init__(self):
        # Find state.json in parent directories
        self.state_file = self._find_state_file()
    
    def _find_state_file(self) -> Optional[Path]:
        """Find state.json by walking up directories"""
        current = Path(__file__).parent
        for _ in range(5):
            state_path = current / "state.json"
            if state_path.exists():
                logger.info(f"Found state.json at: {state_path}")
                return state_path
            current = current.parent
        logger.warning("Could not find state.json - checked up to 5 parent directories")
        return None
    
    def load_state(self) -> Dict:
        """Load current state from file"""
        if not self.state_file or not self.state_file.exists():
            return {
                "state": "idle",
                "detail": "待命中...",
                "progress": 0,
                "updated_at": datetime.now().isoformat()
            }
        
        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading state.json: {e}")
            return {"state": "idle"}
    
    def save_state(self, state: Dict) -> bool:
        """Save state to file"""
        if not self.state_file:
            logger.error("State file path not found")
            return False
        
        try:
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
            logger.info(f"State saved: {state.get('state')} - {state.get('detail')}")
            return True
        except Exception as e:
            logger.error(f"Error saving state.json: {e}")
            return False
    
    def update_state(self, new_state: str, detail: str = "") -> bool:
        """Update the state and save to file"""
        if new_state not in {"idle", "writing", "researching", "executing", "syncing", "error"}:
            logger.warning(f"Invalid state: {new_state}")
            return False
        
        state = self.load_state()
        state["state"] = new_state
        if detail:
            state["detail"] = detail
        state["updated_at"] = datetime.now().isoformat()
        
        return self.save_state(state)

class PrismAlerts:
    """Main alert orchestration"""
    
    def __init__(self):
        self.client = PrismClient()
        self.alerts = AlertManager()
        self.filter = TokenFilter()
        self.state_manager = StateManager()
        self.poll_interval = int(os.getenv('POLL_INTERVAL', 30))
        self.office_url = os.getenv('OFFICE_UI_URL', 'http://127.0.0.1:18791')
        self.agent_name = os.getenv('OFFICE_UI_AGENT_NAME', 'trading-bot')
        self.previous_tokens = set()
        self.last_state_update = 0
        self.state_update_interval = 30  # Update UI state every 30 seconds
    
    def format_currency(self, value: float) -> str:
        """Format value as currency"""
        if value >= 1_000_000:
            return f"${value/1_000_000:.2f}M"
        elif value >= 1_000:
            return f"${value/1_000:.2f}K"
        else:
            return f"${value:.0f}"
    
    def watch_tokens(self):
        """Continuously watch for token alerts"""
        logger.info(f"Starting token watch (polling every {self.poll_interval}s)")
        logger.info("🚀 Prism Alerts monitoring active - Character will appear on token detection")
        
        try:
            while True:
                bonding = self.client.get_bonding_tokens()
                
                found_new_tokens = False
                for token in bonding:
                    if self.filter.should_alert(token, 'bonding'):
                        if token.token_id not in self.previous_tokens:
                            found_new_tokens = True
                            message = self.alerts.format_new_launch_alert(token)
                            self.alerts.send_alert(message, token, 'new_launch')
                            self.update_office_status(token)
                    
                    self.previous_tokens.add(token.token_id)
                
                # Periodically update state to show active monitoring
                current_time = time.time()
                if current_time - self.last_state_update >= self.state_update_interval:
                    if not found_new_tokens:
                        token_count = len(bonding)
                        self.state_manager.update_state(
                            "syncing",
                            f"🔍 Monitoring {token_count} tokens on bonding curve..."
                        )
                    self.last_state_update = current_time
                
                time.sleep(self.poll_interval)
        
        except KeyboardInterrupt:
            logger.info("Watch stopped by user")
            self.state_manager.update_state("idle", "Watch stopped")
        except Exception as e:
            logger.error(f"Error in watch loop: {e}")
            self.state_manager.update_state("error", f"Watch error: {str(e)[:50]}")
    
    def update_office_status(self, token: Token):
        """Update Star Office UI agent status 📊"""
        try:
            detail = f"🚀 Token Alert: ${token.symbol} | MC: {self.format_currency(token.market_cap)} | Holders: {token.holders}"
            
            # Update state.json directly
            success = self.state_manager.update_state("executing", detail)
            if success:
                logger.info(f"✅ Office UI updated - Character shown on screen!")
            
            # Also try HTTP endpoint (for compatibility with external agents)
            try:
                payload = {
                    'agent': self.agent_name,
                    'state': 'executing',
                    'status': detail
                }
                requests.post(f"{self.office_url}/agent-push", json=payload, timeout=5)
            except:
                pass  # Silently fail if office UI not reachable
                
        except Exception as e:
            logger.error(f"Error updating office status: {e}")

def print_tokens_table(tokens: List[Token], title: str):
    """Print tokens in a formatted table"""
    print(f"\n{'=' * 100}")
    print(f"{title}")
    print(f"{'=' * 100}")
    print(f"{'Symbol':<15} {'Name':<25} {'Market Cap':<15} {'Holders':<10} {'Progress':<12} {'Status':<15}")
    print(f"{'-' * 100}")
    
    for token in tokens:
        try:
            progress = f"{token.bonding_progress:.1f}%" if token.bonding_progress < 100 else "100%"
            mc_str = f"${token.market_cap/1000:.1f}K" if token.market_cap >= 1000 else f"${token.market_cap:.0f}"
            
            # Handle special characters
            symbol = token.symbol[:15].encode('utf-8', errors='replace').decode('utf-8')
            name = token.name[:25].encode('utf-8', errors='replace').decode('utf-8')
            
            print(f"{symbol:<15} {name:<25} {mc_str:<15} {token.holders:<10} {progress:<12} {token.status:<15}")
        except Exception as e:
            # Skip tokens with problematic names
            logger.debug(f"Could not print token {token.symbol}: {e}")
            continue
    
    print(f"{'=' * 100}\n")

def main():
    """Main CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: python alerts.py <command> [options]")
        print("\nCommands:")
        print("  bonding      - Show current bonding curve tokens")
        print("  graduated    - Show recently graduated tokens")
        print("  watch        - Watch for new tokens (polling mode)")
        print("  trending     - Show trending tokens")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    alerts_app = PrismAlerts()
    
    if command == 'bonding':
        tokens = alerts_app.client.get_bonding_tokens()
        print_tokens_table(tokens, "Current Bonding Curve Tokens")
    
    elif command == 'graduated':
        tokens = alerts_app.client.get_graduated_tokens()
        print_tokens_table(tokens, "Recently Graduated Tokens")
    
    elif command == 'watch':
        alerts_app.watch_tokens()
    
    elif command == 'trending':
        # Combine both for trending view
        bonding = alerts_app.client.get_bonding_tokens()[:25]
        graduated = alerts_app.client.get_graduated_tokens()[:10]
        
        print_tokens_table(bonding, "Top Trending Tokens (Bonding)")
        print_tokens_table(graduated, "Recent Graduations")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
