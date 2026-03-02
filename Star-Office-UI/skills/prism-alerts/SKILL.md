---
name: prism-alerts
description: Real-time Pump.fun token alerts for Solana traders. Monitor new launches, graduations, and volume spikes with PRISM API integration.
version: 1.1.2
keywords: pumpfun, solana, memecoin, token-alerts, trading-bot, crypto-alerts, solana-trading, real-time-alerts, ai-agent, automation, defi, web3
---

# Pump.fun Alert Bot for Star Office UI

Real-time alerts for Pump.fun token launches, graduations, and volume spikes on Solana. Perfect for trading bots, Discord alerts, Telegram notifications, and AI agents.

## Quick Start

### 1. Installation

```bash
# From project root
cd skills/prism-alerts
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the `prism-alerts` directory:

```bash
PRISM_URL=https://strykr-prism.up.railway.app
TELEGRAM_BOT_TOKEN=your_token_here (optional)
TELEGRAM_CHANNEL_ID=your_channel_id (optional)
DISCORD_BOT_TOKEN=your_token_here (optional)
DISCORD_CHANNEL_ID=your_channel_id (optional)
POLL_INTERVAL=30
MIN_MARKET_CAP=5000
MAX_MARKET_CAP=100000
ENABLE_TELEGRAM=false
ENABLE_DISCORD=false
```

### 3. Usage

```bash
# Get current bonding tokens
python alerts.py bonding

# Get recently graduated tokens
python alerts.py graduated

# Watch for new tokens (polls every 30s by default)
python alerts.py watch

# Get trending tokens
python alerts.py trending
```

## Features

### Real-Time Data Source

PRISM is one of the **only APIs** with real-time Pump.fun bonding curve data:

| Endpoint | Description | Speed |
|----------|-------------|-------|
| `/crypto/trending/solana/bonding` | Tokens on bonding curve | 648ms |
| `/crypto/trending/solana/graduated` | Graduated to DEX | 307ms |

### Alert Types

#### 1. New Launch Alert
```
🚀 NEW PUMP.FUN TOKEN

$DOGWIFCAT
CA: 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU

📊 Stats:
• Bonding Progress: 12%
• Market Cap: $8,450
• Holders: 23
• Created: 2 min ago

[🔍 Scan] [📈 Chart] [💰 Buy]
```

#### 2. Graduation Alert
```
🎓 TOKEN GRADUATED!

$MEMECOIN just graduated to Raydium!

📊 Final Stats:
• Market Cap: $69,000
• Total Holders: 1,247
• Bonding Time: 4h 23m

Trading now live on Raydium DEX
[📈 Trade on Raydium]
```

#### 3. Volume Spike Alert
```
📈 VOLUME SPIKE DETECTED

$CATDOG seeing unusual activity

• Volume (5m): $45,230 (+340%)
• Price: +28% in 10 minutes
• New holders: +89

⚠️ Could be coordinated buy - DYOR
[🔍 Scan] [📈 Chart]
```

## Python API Usage

```python
from alerts import PrismClient, AlertManager

# Initialize client
client = PrismClient()

# Get bonding tokens
bonding = client.get_bonding_tokens()
for token in bonding:
    print(f"${token['symbol']}: MC=${token['market_cap']}, Holders={token['holders']}")

# Get graduated tokens
graduated = client.get_graduated_tokens()

# Initialize alert manager
alert_mgr = AlertManager()

# Send Telegram alert
alert_mgr.send_telegram_alert("Your alert message")

# Send Discord alert
alert_mgr.send_discord_alert("Your alert message")
```

## Integration with Star Office UI

This skill can be used with Star Office UI to:
- Monitor trading activity in the office dashboard
- Send alerts about token market changes to agents
- Update agent status when trades occur
- Track trading metrics in daily summaries

### Example: Update Office Status on Alert

```python
import requests

# When a high-volume token is detected
def on_volume_spike(token):
    # Send alert
    alert_mgr.send_telegram_alert(f"Volume spike: {token['symbol']}")
    
    # Update Star Office UI agent status
    requests.post('http://127.0.0.1:18791/set-state', json={
        'agent': 'trading-bot',
        'state': 'executing',
        'status': f'Monitoring {token["symbol"]} - Volume spike detected'
    })
```

## Best Practices

1. **Rate Limiting**: Poll max once per 30 seconds
2. **Deduplication**: Track sent alerts in SQLite/Redis to avoid duplicates
3. **Batching**: Group multiple alerts into one message
4. **Cooldowns**: Don't spam same token within 5 minutes
5. **Filter by Market Cap**: Set MIN_MARKET_CAP and MAX_MARKET_CAP to avoid noise

## Architecture

```
prism-alerts/
├── alerts.py          # Main CLI and API wrapper
├── client.py          # PRISM API client
├── alert_manager.py   # Alert routing and formatting
├── filters.py         # Token filtering logic
├── db.py              # Alert deduplication database
├── requirements.txt   # Python dependencies
├── .env.example       # Environment variables template
└── SKILL.md           # This file
```

## Troubleshooting

### No alerts appearing?
- Check PRISM_URL is correct and accessible
- Verify ENABLE_TELEGRAM or ENABLE_DISCORD is set correctly
- Check bot tokens are valid

### Rate limits?
- Increase POLL_INTERVAL to 60+ seconds
- Use alert deduplication to avoid spam

### Missing tokens?
- Check MIN_MARKET_CAP and MAX_MARKET_CAP settings
- Verify token hasn't been filtered by age or holder count

## Support

- GitHub: [NextFrontierBuilds/prism-alerts-skill](https://github.com/NextFrontierBuilds/prism-alerts-skill)
- Author: [@NextXFrontier](https://x.com/NextXFrontier)
- Star Office UI: [ringhyacinth/Star-Office-UI](https://github.com/ringhyacinth/Star-Office-UI)

