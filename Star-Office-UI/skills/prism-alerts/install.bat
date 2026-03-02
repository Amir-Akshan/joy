@echo off
REM Prism Alerts Installation Script for Windows
REM Quick setup for Pump.fun token monitoring in Star Office UI

echo ==========================================
echo Prism Alerts - Pump.fun Token Monitor
echo Installation Script for Windows
echo ==========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo Step 1: Installing Python dependencies...
pip install -r requirements.txt
echo ✓ Dependencies installed
echo.

echo Step 2: Creating environment file...
if not exist .env (
    copy .env.example .env
    echo ✓ Created .env file (edit with your settings)
) else (
    echo ⚠ .env already exists, skipping...
)
echo.

echo Step 3: Setting up alert database...
python alerts.py bonding > nul 2>&1
if exist alerts.db (
    echo ✓ Database initialized
) else (
    echo ⚠ Database will be created on first run
)
echo.

echo ==========================================
echo ✓ Installation Complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Edit .env file with your PRISM_URL and alert settings
echo 2. (Optional) Configure Telegram: ENABLE_TELEGRAM=true
echo 3. (Optional) Configure Discord: ENABLE_DISCORD=true
echo 4. Test: python alerts.py bonding
echo 5. Run: python alerts.py watch
echo.
echo Documentation: README.md
echo Examples: python examples.py
echo.
pause
