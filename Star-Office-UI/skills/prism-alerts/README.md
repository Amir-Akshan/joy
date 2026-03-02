# Prism Alerts - Pump.fun Token Alerts for Star Office UI

Real-time alerts for Solana token launches, graduations, and volume spikes using the Strykr PRISM API.

## Features

✨ **Real-Time Monitoring**
- Track Pump.fun bonding curve tokens in real-time
- Monitor token graduations to DEX
- Detect volume spikes automatically

🎯 **Smart Alerts**
- Configurable market cap filters
- Holder count thresholds
- Bonding progress monitoring
- Automatic cooldowns to prevent spam

🔔 **Multi-Channel Delivery**
- Telegram bot integration
- Discord webhook support
- Console output
- Star Office UI agent status updates

## Installation

### Step 1: Create Environment File

```bash
cd skills/prism-alerts
cp .env.example .env
```

### Step 2: Configure the .env file

Edit `.env` with your settings:

```bash
# Required
PRISM_URL=https://strykr-prism.up.railway.app

# Optional: Telegram alerts
ENABLE_TELEGRAM=false
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHANNEL_ID=your_channel_id

# Optional: Discord alerts
ENABLE_DISCORD=false
DISCORD_BOT_TOKEN=your_bot_token
DISCORD_CHANNEL_ID=your_channel_id

# Alert filters
MIN_MARKET_CAP=5000
MAX_MARKET_CAP=100000
MIN_HOLDERS=10
POLL_INTERVAL=30
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### View Current Bonding Tokens

```bash
python alerts.py bonding
```

Output:
```
====================================================================================================
Current Bonding Curve Tokens
====================================================================================================
Symbol          Name                      Market Cap      Holders    Progress    Status         
----------------------------------------------------------------------------------------------------
$DOGWIF         DOGWIFCAT                 $8.5K           23         12.0%       bonding        
$MEMECOIN       Memecoin                  $15.3K          45         28.5%       bonding        
...
```

### View Recently Graduated Tokens

```bash
python alerts.py graduated
```

### Watch for New Tokens (Polling Mode)

This continuously monitors for new tokens and sends alerts when matches are found:

```bash
python alerts.py watch
```

The watch mode will:
1. Poll PRISM API every 30 seconds (configurable)
2. Filter tokens based on market cap, holders, etc.
3. Send alerts via Telegram/Discord if configured
4. Update Star Office UI agent status
5. Prevent duplicate alerts with cooldowns

### View Trending Tokens

```bash
python alerts.py trending
```

Shows top bonding tokens and recent graduations combined.

## Integration with Star Office UI

When a new high-potential token is detected, the bot automatically updates your Star Office UI trading agent status:

```
Agent: trading-bot
State: executing
Status: Monitoring $DOGWIF - Market Cap: $8.5K
```

This helps visualize real-time trading activity in your office dashboard.

## Configuration Options

| Setting | Default | Description |
|---------|---------|-------------|
| PRISM_URL | [https://strykr-prism.up.railway.app](https://strykr-prism.up.railway.app) | PRISM API endpoint |
| POLL_INTERVAL | 30 | Seconds between API polls |
| MIN_MARKET_CAP | 5000 | Minimum market cap to alert |
| MAX_MARKET_CAP | 100000 | Maximum market cap to alert (prevents spam) |
| MIN_HOLDERS | 10 | Minimum holder count to alert |
| BONDING_PROGRESS_THRESHOLD | 20 | Minimum bonding progress % to alert |
| ENABLE_TELEGRAM | false | Enable Telegram alerts |
| ENABLE_DISCORD | false | Enable Discord alerts |

## Architecture

```
alerts.py
├── PrismClient         → Fetches data from PRISM API
├── AlertDatabase       → SQLite deduplication & cooldowns
├── AlertManager        → Formats & sends alerts
├── TokenFilter         → Applies market filters
└── PrismAlerts         → Main orchestration
```

## Best Practices

1. **Set Realistic Filters**: Adjust MIN/MAX market cap to avoid alert fatigue
2. **Use Cooldowns**: Default 5-minute cooldown prevents spam for same token
3. **Enable Deduplication**: Database automatically tracks sent alerts
4. **Poll Responsibly**: 30 seconds is safe; avoid < 10 seconds
5. **Monitor Telegram/Discord Bot Rate Limits**: 30 msg/second per bot is typical

## Troubleshooting

### No alerts appearing

1. Check PRISM API is accessible:
   ```bash
   curl https://strykr-prism.up.railway.app/status
   ```

2. Verify bot tokens (if using Telegram/Discord):
   ```bash
   grep TELEGRAM_BOT_TOKEN .env
   python -c "import os; from dotenv import load_dotenv; load_dotenv('.env'); print(os.getenv('TELEGRAM_BOT_TOKEN'))"
   ```

3. Check market cap filters aren't too restrictive:
   ```bash
   python alerts.py bonding  # See what tokens exist
   ```

### Too many alerts (spam)

- Increase MIN_MARKET_CAP
- Increase MIN_HOLDERS
- Decrease BONDING_PROGRESS_THRESHOLD (requires more mature tokens)
- Adjust POLL_INTERVAL to 60+ seconds

### Star Office UI not updating

- Verify OFFICE_UI_URL is correct (default: http://127.0.0.1:18791)
- Ensure Star Office backend is running
- Check OFFICE_UI_AGENT_NAME matches an existing agent

## Development

### Adding Custom Filters

Edit `TokenFilter` class in `alerts.py`:

```python
def should_alert(self, token: Token, token_type: str = 'bonding') -> bool:
    # Add your custom logic
    if token.symbol.startswith('$'):  # Example filter
        return False
    return True
```

### Custom Alert Formatting

Override `AlertManager.format_new_launch_alert()`:

```python
def format_new_launch_alert(self, token: Token) -> str:
    return f"Custom format: {token.symbol} ${token.market_cap}"
```

## API Reference

### PrismClient

```python
client = PrismClient()

# Get bonding tokens
tokens = client.get_bonding_tokens(limit=50)

# Get graduated tokens
tokens = client.get_graduated_tokens(limit=50)
```

### AlertManager

```python
alerts = AlertManager()

# Send alert through all configured channels
alerts.send_alert(message, token, alert_type='new_launch')

# Send specific channel
alerts.send_telegram_alert(message)
alerts.send_discord_alert(message)
```

## License

MIT License - Built for Pump.fun & Solana community

## Credits

- **PRISM API**: [Strykr](https://strykr.com)
- **Author**: [Next Frontier](https://x.com/NextXFrontier)
- **Integrated with**: [Star Office UI](https://github.com/ringhyacinth/Star-Office-UI)

