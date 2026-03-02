# Prism Alerts Integration with Star Office UI

This guide explains how to integrate **Prism Alerts** (Pump.fun token monitoring) with Star Office UI.

## What is Prism Alerts?

Prism Alerts is a real-time monitoring system for Solana Pump.fun tokens that can:
- Monitor bonding curve tokens
- Detect token graduations
- Identify volume spikes
- Send alerts via Telegram, Discord, or console
- Update Office UI agent status in real-time

## Integration Points

### 1. Agent Status Updates

When a high-potential token is detected, Prism Alerts automatically updates your Star Office UI trading agent:

```python
# alerts.py sends to Star Office UI
requests.post('http://127.0.0.1:18791/agent-push', json={
    'agent': 'trading-bot',
    'state': 'executing',
    'status': 'Monitoring $DOGWIF - MC: $8.5K'
})
```

This makes your trading activity visible in the office dashboard.

### 2. Multi-Channel Alerts

Prism Alerts can send token alerts through multiple channels simultaneously:
- **Console Output**: Always enabled, useful for development
- **Telegram**: For mobile notifications
- **Discord**: For team coordination
- **Office UI**: For visual dashboard updates

### 3. Smart Filtering

Only relevant tokens trigger alerts based on:
- Market cap range (default: $5K - $100K)
- Holder count (minimum: 10)
- Bonding progress (minimum: 20%)
- Cooldown periods (5 min default to prevent spam)

## Setup Instructions

### Step 1: Install Dependencies

```bash
cd skills/prism-alerts
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
cp .env.example .env
nano .env  # or use your favorite editor
```

Essential settings:

```bash
# Required
PRISM_URL=https://strykr-prism.up.railway.app

# Office UI integration (should match your setup)
OFFICE_UI_URL=http://127.0.0.1:18791
OFFICE_UI_AGENT_NAME=trading-bot

# Optional: Telegram
ENABLE_TELEGRAM=false
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHANNEL_ID=your_channel_here

# Optional: Discord
ENABLE_DISCORD=false
DISCORD_BOT_TOKEN=your_token_here
DISCORD_CHANNEL_ID=your_channel_here

# Filters
MIN_MARKET_CAP=5000
MAX_MARKET_CAP=100000
POLL_INTERVAL=30
```

### Step 3: Test the Integration

```bash
# View available bonding tokens
python alerts.py bonding

# View recently graduated tokens
python alerts.py graduated

# Run examples (no Office UI required)
python examples.py
```

### Step 4: Start Monitoring

With Star Office UI running:

```bash
# Make sure backend is running
cd ../../backend
python app.py

# In another terminal, start Prism Alerts
cd ../skills/prism-alerts
python alerts.py watch
```

## Usage Patterns

### Pattern 1: Manual Checks

Check tokens on demand without continuous monitoring:

```bash
# During work breaks
python alerts.py bonding    # See what's hot now
python alerts.py graduated  # Recent launches that succeeded
```

### Pattern 2: Continuous Monitoring

Run in the background for 24/7 coverage:

```bash
# Terminal 1: Star Office UI backend
cd backend && python app.py

# Terminal 2: Prism Alerts watching
cd skills/prism-alerts && python alerts.py watch

# Check Office UI dashboard at http://127.0.0.1:18791
```

### Pattern 3: Scheduled Alerts

Use cron (Linux/Mac) or Task Scheduler (Windows):

```bash
# Check every hour
0 * * * * cd /path/to/skills/prism-alerts && python alerts.py bonding >> alerts.log 2>&1

# Check every 6 hours
0 */6 * * * cd /path/to/skills/prism-alerts && python alerts.py graduated >> alerts.log 2>&1
```

### Pattern 4: Telegram Notifications

Get mobile alerts for new high-potential tokens:

```bash
# .env settings
ENABLE_TELEGRAM=true
TELEGRAM_BOT_TOKEN=123456789:ABCDEFGHIJKLMNOPQRSTUVWxyz
TELEGRAM_CHANNEL_ID=-12345678

# Run monitoring
python alerts.py watch
```

## API Integration

### Python SDK

```python
from skills.prism_alerts.alerts import PrismClient, AlertManager

# Create client
client = PrismClient()

# Get tokens
bonding_tokens = client.get_bonding_tokens()
graduated_tokens = client.get_graduated_tokens()

# Send alerts
alert_mgr = AlertManager()
alert_mgr.send_telegram_alert("New token: $DOGWIF")
alert_mgr.send_discord_alert("Token graduated!")
```

### REST API via Office UI

Prism Alerts integrates with Office UI's `/agent-push` endpoint:

```bash
curl -X POST http://127.0.0.1:18791/agent-push \
  -H "Content-Type: application/json" \
  -d '{
    "agent": "trading-bot",
    "state": "executing",
    "status": "Monitoring 5 tokens on bonding curve"
  }'
```

## Troubleshooting

### Problem: No tokens showing

**Solution**: Check PRISM_URL is accessible:

```bash
curl https://strykr-prism.up.railway.app/crypto/trending/solana/bonding
```

### Problem: Too many/few alerts

**Solution**: Adjust filters in `.env`:

```bash
# For fewer alerts (stricter filtering)
MIN_MARKET_CAP=10000       # Increase minimum
MAX_MARKET_CAP=50000       # Lower maximum  
MIN_HOLDERS=25             # More holders required
BONDING_PROGRESS_THRESHOLD=30  # More matured tokens

# For more alerts (looser filtering)
MIN_MARKET_CAP=1000        # Lower minimum
MIN_HOLDERS=5              # Fewer holders required
BONDING_PROGRESS_THRESHOLD=10  # Newer tokens too
```

### Problem: Office UI not updating

**Solution**: Verify Office UI is running:

```bash
# Check if Office UI is accessible
curl http://127.0.0.1:18791/status

# Verify endpoint exists
curl -X POST http://127.0.0.1:18791/agent-push \
  -H "Content-Type: application/json" \
  -d '{"agent":"test","state":"idle","status":"test"}'
```

### Problem: Telegram/Discord alerts not working

**Solution**: Verify bot tokens:

```python
# Test Telegram
import requests
token = "YOUR_TELEGRAM_BOT_TOKEN"
url = f"https://api.telegram.org/bot{token}/getMe"
print(requests.get(url).json())

# Test Discord  
import requests
token = "YOUR_DISCORD_BOT_TOKEN"
url = "https://discordapp.com/api/users/@me"
headers = {'Authorization': f'Bot {token}'}
print(requests.get(url, headers=headers).json())
```

## Performance Considerations

### Polling Interval

- **10-15 seconds**: Very aggressive, may hit rate limits
- **30 seconds** (default): Good balance for most use cases
- **60+ seconds**: Conservative, misses quick opportunities

### Database Size

The `alerts.db` SQLite database stores alert history:
- Typical size: <1MB for weeks of data
- Automatic cleanup not implemented (you can delete it to reset)
- Used for deduplication and cooldown tracking

### Memory Usage

Prism Alerts typically uses:
- ~50-100MB idle (waiting for polls)
- Spikes to ~150MB during API calls
- Well-suited for any modern computer

## Advanced Customization

### Custom Alert Formats

Edit `alerts.py` AlertManager class:

```python
def format_new_launch_alert(self, token: Token) -> str:
    return f"🚀 {token.symbol} | MC: ${token.market_cap:,.0f}"
```

### Custom Filters

Override TokenFilter logic:

```python
class CustomFilter(TokenFilter):
    def should_alert(self, token, token_type='bonding'):
        # Only tokens with 'DOG' in name
        if 'DOG' not in token.symbol.upper():
            return False
        return super().should_alert(token, token_type)
```

### Database Persistence

Use SQLAlchemy for custom storage:

```python
from sqlalchemy import create_engine
engine = create_engine('postgresql://user:pass@localhost/alerts')
```

## Architecture

```
skills/prism-alerts/
├── alerts.py              # Main app & CLI
├── examples.py            # Quick start examples
├── requirements.txt       # Python dependencies
├── skill.json            # Metadata for skills registry
├── .env.example          # Configuration template
├── config.json           # Integration mappings
├── README.md             # User documentation
└── INTEGRATION.md        # This file
```

## Contributing

We welcome improvements! Areas for enhancement:

- [ ] WebSocket support for real-time updates
- [ ] Custom notification templates
- [ ] Multi-chain support (Ethereum, Base, etc.)
- [ ] Machine learning for token prediction
- [ ] Web UI dashboard
- [ ] Historical data analysis

## License

MIT - Free to use and modify

## Support

- **Issues**: [prism-alerts-skill](https://github.com/NextFrontierBuilds/prism-alerts-skill/issues)
- **Author**: [@NextXFrontier](https://x.com/NextXFrontier)
- **Star Office UI**: [ringhyacinth](https://github.com/ringhyacinth/Star-Office-UI)

---

**Remember**: DYOR (Do Your Own Research) before making any trades! Alerts are informational only.
