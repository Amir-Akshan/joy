# Prism Alerts - Quick Setup Guide

## ✅ Installation Complete!

Your Pump.fun token monitoring skill has been successfully integrated into Star Office UI.

### 📂 What Was Created

```
skills/
├── README.md                           # Skills documentation hub
└── prism-alerts/                       # Token monitoring skill
    ├── alerts.py                       # Main application (Python)
    ├── examples.py                     # Quick examples
    ├── test_alerts.py                  # Unit tests
    ├── requirements.txt                # Python dependencies
    ├── skill.json                      # Skill metadata
    ├── .env.example                    # Configuration template
    ├── README.md                       # User documentation
    ├── SKILL.md                        # Detailed skill guide
    ├── INTEGRATION.md                  # Office UI integration
    ├── config.json                     # Integration mappings
    ├── Dockerfile                      # Container setup
    ├── docker-compose.yml              # Docker compose file
    ├── install.sh                      # Linux/Mac installer
    ├── install.bat                     # Windows installer
    └── verify_installation.py          # Verification script
```

### 🚀 Quick Start (2 minutes)

#### Step 1: Setup Environment

```bash
cd skills/prism-alerts

# Copy template
cp .env.example .env

# Edit .env with your settings (or use defaults)
# nano .env
```

#### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 3: Verify Installation

```bash
python verify_installation.py
```

#### Step 4: Test Connection

```bash
python alerts.py bonding
```

Should show tokens like:
```
==================================================
Current Bonding Curve Tokens
==================================================
Symbol    Name              MC        Holders  Progress
--------------------------------------------------
$DOGWIF   DOGWIFCAT         $8.5K     23       12.0%
$MEMECOIN Memecoin          $15.3K    45       28.5%
...
```

#### Step 5: Start Monitoring

First, make sure Star Office UI backend is running:

```bash
# In one terminal
cd backend
python app.py
```

Then in another terminal, start Prism Alerts:

```bash
cd skills/prism-alerts
python alerts.py watch
```

Open http://127.0.0.1:18791 and you'll see the agent status updating!

### 📊 Available Commands

```bash
python alerts.py bonding        # View bonding curve tokens
python alerts.py graduated      # View graduated tokens
python alerts.py trending       # Combined trending view
python alerts.py watch          # Start continuous monitoring

python examples.py              # Run example scenarios
python verify_installation.py   # Verify setup
python test_alerts.py           # Run unit tests
```

### 🔧 Configuration

Edit `.env` to customize:

```bash
# PRISM API
PRISM_URL=https://strykr-prism.up.railway.app

# Star Office UI (auto-detects if localhost)
OFFICE_UI_URL=http://127.0.0.1:18791
OFFICE_UI_AGENT_NAME=trading-bot

# Token Filters
MIN_MARKET_CAP=5000
MAX_MARKET_CAP=100000
MIN_HOLDERS=10
POLL_INTERVAL=30

# Optional: Telegram Alerts
ENABLE_TELEGRAM=false
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHANNEL_ID=your_channel

# Optional: Discord Alerts
ENABLE_DISCORD=false
DISCORD_BOT_TOKEN=your_token
DISCORD_CHANNEL_ID=your_channel
```

### 🐳 Docker Deployment

```bash
# Build image
docker build -t prism-alerts .

# Run container
docker run -e OFFICE_UI_URL=http://host.docker.internal:18791 prism-alerts

# Or use docker-compose
docker-compose up -d
```

### 📖 Documentation

- **[README.md](README.md)** - Full user guide with examples
- **[INTEGRATION.md](INTEGRATION.md)** - Integration with Office UI
- **[SKILL.md](SKILL.md)** - Detailed skill specifications
- **[skill.json](skill.json)** - Skill metadata
- **[config.json](config.json)** - Integration configuration

### 🧪 Testing

```bash
# Run examples
python examples.py

# Run unit tests
python test_alerts.py

# Verify installation
python verify_installation.py
```

### 🛠️ Troubleshooting

#### "No tokens appearing?"
```bash
# Check PRISM API is accessible
curl https://strykr-prism.up.railway.app/crypto/trending/solana/bonding

# Check filters aren't blocking everything
python alerts.py bonding
```

#### "Office UI not updating?"
```bash
# Make sure backend is running
curl http://127.0.0.1:18791/health

# Check OFFICE_UI_URL is correct in .env
```

#### "Too many/few alerts?"
Adjust `MIN_MARKET_CAP`, `MAX_MARKET_CAP`, `MIN_HOLDERS` in `.env`

#### "Telegram/Discord not working?"
- Get bot token from @BotFather (Telegram) or Discord bot settings
- Verify `ENABLE_TELEGRAM=true` or `ENABLE_DISCORD=true`
- Test tokens are valid

### 📚 Learning Resources

- [Pump.fun Official](https://pump.fun)
- [PRISM API Documentation](https://strykr-prism.up.railway.app)
- [Solana Developer Guide](https://docs.solana.com)
- [Star Office UI](https://github.com/ringhyacinth/Star-Office-UI)

### 👥 Support

- **Issues**: [Prism Alerts GitHub](https://github.com/NextFrontierBuilds/prism-alerts-skill/issues)
- **Author**: [@NextXFrontier](https://x.com/NextXFrontier)
- **Star Office UI**: [@ring_hyacinth](https://x.com/ring_hyacinth)

### 📄 Files Reference

| File | Purpose |
|------|---------|
| `alerts.py` | Main CLI application |
| `examples.py` | Quick start examples |
| `test_alerts.py` | Unit tests |
| `requirements.txt` | Python dependencies |
| `.env.example` | Config template |
| `skill.json` | Skill metadata |
| `README.md` | Full documentation |
| `INTEGRATION.md` | Office UI integration |
| `Dockerfile` | Container image |
| `docker-compose.yml` | Docker setup |

### ✅ Verification Checklist

- [ ] Files created in `skills/prism-alerts/`
- [ ] `.env` copied from `.env.example`
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Connection verified (`python alerts.py bonding`)
- [ ] Office UI backend running on http://127.0.0.1:18791
- [ ] Alert tests passed (`python examples.py`)
- [ ] Ready to start monitoring (`python alerts.py watch`)

---

**Remember**: DYOR (Do Your Own Research) before any trades!

Happy trading! 🚀
