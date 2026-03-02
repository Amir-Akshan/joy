#!/usr/bin/env python3
"""
Prism Alerts - Installation & Setup Verification
Verify that all components are correctly installed
"""

import os
import sys
from pathlib import Path

def check_file_exists(path: str, name: str) -> bool:
    """Check if a file exists"""
    exists = os.path.exists(path)
    status = "✓" if exists else "✗"
    print(f"{status} {name}: {path}")
    return exists

def check_directory(path: str, name: str) -> bool:
    """Check if a directory exists"""
    exists = os.path.isdir(path)
    status = "✓" if exists else "✗"
    print(f"{status} {name}: {path}")
    return exists

def main():
    """Main verification script"""
    
    print("\n" + "="*60)
    print("Prism Alerts - Installation Verification")
    print("="*60 + "\n")
    
    base_path = Path(__file__).parent
    
    # Check essential files
    print("Essential Files:")
    print("-" * 60)
    files_ok = True
    files_ok &= check_file_exists(base_path / "alerts.py", "Main application")
    files_ok &= check_file_exists(base_path / "requirements.txt", "Dependencies")
    files_ok &= check_file_exists(base_path / "skill.json", "Skill metadata")
    files_ok &= check_file_exists(base_path / ".env.example", "Environment template")
    files_ok &= check_file_exists(base_path / "README.md", "Documentation")
    files_ok &= check_file_exists(base_path / "INTEGRATION.md", "Integration guide")
    
    print("\nOptional Files:")
    print("-" * 60)
    check_file_exists(base_path / "__init__.py", "Python module init")
    check_file_exists(base_path / "examples.py", "Example scripts")
    check_file_exists(base_path / "test_alerts.py", "Unit tests")
    check_file_exists(base_path / "docker-compose.yml", "Docker compose")
    check_file_exists(base_path / "Dockerfile", "Docker image")
    
    if not files_ok:
        print("\n✗ Some essential files are missing!")
        return False
    
    print("\n" + "="*60)
    print("Installation Status: ✓ READY TO USE")
    print("="*60)
    
    print("\nNext Steps:")
    print("1. Copy .env.example to .env:")
    print("   cp .env.example .env")
    
    print("\n2. Edit .env with your settings:")
    print("   - PRISM_URL (required)")
    print("   - OFFICE_UI_URL (optional, auto-detects localhost)")
    print("   - TELEGRAM settings (optional)")
    print("   - DISCORD settings (optional)")
    
    print("\n3. Install Python dependencies:")
    print("   pip install -r requirements.txt")
    
    print("\n4. Test the connection:")
    print("   python alerts.py bonding")
    
    print("\n5. Start monitoring (with Office UI running):")
    print("   python alerts.py watch")
    
    print("\n6. More options:")
    print("   python alerts.py graduated    # Recently graduated tokens")
    print("   python alerts.py trending     # Combined trending view")
    print("   python examples.py            # Run example scenarios")
    
    print("\nDocumentation:")
    print("- README.md - Full user guide")
    print("- INTEGRATION.md - Office UI integration details")
    print("- SKILL.md - Skill-specific documentation")
    print("- skill.json - Metadata for registries")
    
    print("\nSupport:")
    print("- GitHub: https://github.com/NextFrontierBuilds/prism-alerts-skill")
    print("- Author: @NextXFrontier on X/Twitter")
    print("- Integrated with: Star Office UI by @ring_hyacinth")
    
    print("\n" + "="*60 + "\n")
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
