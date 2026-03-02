#!/bin/bash
# Prism Alerts Installation Script
# Quick setup for Pump.fun token monitoring in Star Office UI

set -e

echo "=========================================="
echo "Prism Alerts - Pump.fun Token Monitor"
echo "Installation Script"  
echo "=========================================="
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Step 1: Installing Python dependencies..."
cd "$SCRIPT_DIR"

if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found. Please install Python 3.8+ first."
    exit 1
fi

pip3 install -r requirements.txt

echo "✓ Dependencies installed"
echo ""

echo "Step 2: Creating environment file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Created .env file (edit with your settings)"
else
    echo "⚠ .env already exists, skipping..."
fi
echo ""

echo "Step 3: Setting up alert database..."
python3 alerts.py bonding > /dev/null 2>&1 || true
if [ -f alerts.db ]; then
    echo "✓ Database initialized"
else
    echo "⚠ Creating database on first run..."
fi
echo ""

echo "=========================================="
echo "✓ Installation Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your PRISM_URL and alert settings"
echo "2. (Optional) Configure Telegram: ENABLE_TELEGRAM=true"
echo "3. (Optional) Configure Discord: ENABLE_DISCORD=true"
echo "4. Test: python3 alerts.py bonding"
echo "5. Run: python3 alerts.py watch"
echo ""
echo "Documentation: README.md"
echo "Examples: python3 examples.py"
echo ""
