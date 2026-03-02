# Skills Directory

This directory contains optional skills and extensions for Star Office UI.

## Available Skills

### 1. Prism Alerts - Pump.fun Token Monitoring

Real-time alerts for Solana Pump.fun token launches, graduations, and volume spikes.

**Location**: `./prism-alerts/`

**Quick Start**:

```bash
cd prism-alerts
pip install -r requirements.txt
cp .env.example .env
python alerts.py bonding
```

**Key Features**:
- 📊 Real-time bonding curve monitoring
- 🎓 Token graduation detection
- 📈 Volume spike alerts
- 💬 Telegram/Discord integration
- 📍 Office UI agent status updates
- 🔍 Smart token filtering

**Documentation**:
- [README.md](prism-alerts/README.md) - Full documentation
- [INTEGRATION.md](prism-alerts/INTEGRATION.md) - Integration with Office UI
- [skill.json](prism-alerts/skill.json) - Skill metadata

**Commands**:
```bash
python alerts.py bonding       # Get current tokens
python alerts.py graduated     # Get graduated tokens  
python alerts.py watch         # Continuous monitoring
python alerts.py trending      # Trending overview
```

---

## How to Use Skills

### For Users

1. Navigate to a skill directory
2. Install dependencies: `pip install -r requirements.txt`
3. Read the README.md for usage instructions
4. Follow setup guide in INTEGRATION.md (if available)

### For Developers

Skills can be:
- **Standalone**: Run independently as CLI tools or services
- **Integrated**: Update Office UI agent status via `/agent-push` endpoint
- **Collaborative**: Coordinate across multiple agents

### Skill Structure

```
skill-name/
├── README.md              # User documentation
├── SKILL.md               # Skill details (for registries)
├── INTEGRATION.md         # Integration guide (optional)
├── skill.json             # Metadata
├── requirements.txt       # Python dependencies
├── .env.example           # Configuration template
├── main_script.py         # Main implementation
└── tests/                 # Unit tests (optional)
```

## Contributing Your Own Skill

1. Create a new folder in `skills/`
2. Include metadata in `skill.json`
3. Add documentation in `README.md`
4. List integrations if connecting to Office UI
5. Test with multiple platforms (Windows/Mac/Linux)

## Integration Points with Star Office UI

Skills can integrate with Star Office UI through:

### Agent Status Updates

```python
import requests

requests.post('http://127.0.0.1:18791/agent-push', json={
    'agent': 'skill-name',
    'state': 'executing',
    'status': 'Doing something...'
})
```

### States

- `idle` - Waiting
- `writing` - Working actively  
- `researching` - Investigating
- `executing` - Processing
- `syncing` - Coordinating
- `error` - Problem detected

## Future Skills

Planned skills for Star Office UI:

- [ ] **price-tracker** - Crypto price monitoring and alerts
- [ ] **web-crawler** - Automated web scraping and analysis
- [ ] **email-notifier** - Email notification integration
- [ ] **slack-sync** - Slack channel synchronization
- [ ] **github-monitor** - Repository activity tracking
- [ ] **weather-alerts** - Weather and disaster notifications
- [ ] **schedule-manager** - Task and meeting coordination
- [ ] **market-analyzer** - Technical analysis tools

---

**Questions?** Check individual skill documentation or open an issue.
