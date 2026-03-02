#!/usr/bin/env python3
"""
Test Prism Alerts with Star Office UI Character Animation
Demonstrates the character appearing when tokens are detected
"""

import os
import sys
import json
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from alerts import PrismAlerts, StateManager, Token

def test_character_animation():
    """Test showing character with different token states"""
    
    print("\n" + "="*60)
    print("🎬 PRISM ALERTS - CHARACTER ANIMATION TEST")
    print("="*60)
    
    state_mgr = StateManager()
    
    if not state_mgr.state_file:
        print("\n❌ ERROR: Could not find state.json")
        print("   Make sure Star Office UI is in a parent directory")
        return False
    
    print(f"\n✅ Found state.json at: {state_mgr.state_file}")
    
    # Test 1: Show resting state
    print("\n1️⃣  Setting character to IDLE (resting)...")
    state_mgr.update_state("idle", "Taking a break")
    time.sleep(2)
    
    # Test 2: Show working state
    print("2️⃣  Setting character to EXECUTING (token detected!)...")
    state_mgr.update_state("executing", "🚀 Token Found: $DOGWIF | Market Cap: $8.5K")
    time.sleep(2)
    
    # Test 3: Show syncing state
    print("3️⃣  Setting character to SYNCING (monitoring)...")
    state_mgr.update_state("syncing", "🔍 Monitoring 15 tokens on bonding curve")
    time.sleep(2)
    
    # Test 4: Show error state
    print("4️⃣  Setting character to ERROR (something odd)...")
    state_mgr.update_state("error", "⚠️  Unusual activity detected")
    time.sleep(2)
    
    # Test 5: Back to idle
    print("5️⃣  Back to IDLE...")
    state_mgr.update_state("idle", "Standby")
    
    print("\n" + "="*60)
    print("✅ TEST COMPLETE!")
    print("="*60)
    print("\nOpen http://127.0.0.1:18791 in your browser to see the character")
    print("The character should have moved through different areas:")
    print("  • IDLE → sofa (breakroom)")
    print("  • EXECUTING → desk (working)")
    print("  • SYNCING → desk (working)")
    print("  • ERROR → server room")
    print("\n")
    
    return True

def test_real_monitoring():
    """Test real token monitoring with character animation"""
    
    print("\n" + "="*60)
    print("🚀 PRISM ALERTS - REAL MONITORING WITH CHARACTER")
    print("="*60)
    print("\nStarting real token monitor...")
    print("The character will appear when tokens are found!")
    print("Press Ctrl+C to stop\n")
    
    alerts = PrismAlerts()
    
    if not alerts.state_manager.state_file:
        print("❌ Cannot find state.json - make sure parent directory is correct")
        return False
    
    print(f"✅ Using state.json: {alerts.state_manager.state_file}\n")
    
    # Start watching
    try:
        alerts.watch_tokens()
    except KeyboardInterrupt:
        print("\n\n✅ Monitoring stopped")
        alerts.state_manager.update_state("idle", "Monitor stopped")

def main():
    """Main test menu"""
    
    if len(sys.argv) < 2:
        print("\n" + "="*60)
        print("PRISM ALERTS - TEST SUITE")
        print("="*60)
        print("\nUsage: python test_animation.py <command>")
        print("\nCommands:")
        print("  1  - Test character animation (shows all states)")
        print("  2  - Real monitoring (live token detection)")
        print("\nExample:")
        print("  python test_animation.py 1")
        print("  python test_animation.py 2")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "1":
        test_character_animation()
    elif command == "2":
        test_real_monitoring()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
