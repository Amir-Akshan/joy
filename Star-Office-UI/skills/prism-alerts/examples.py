#!/usr/bin/env python3
"""
PRISM Alerts - Quick Start Examples
Real-time token monitoring for Pump.fun
"""

import os
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

from alerts import PrismClient, AlertManager, TokenFilter

def example_1_get_bonding_tokens():
    """Example 1: Get current bonding curve tokens"""
    print("\n" + "="*50)
    print("Example 1: Get Bonding Tokens")
    print("="*50)
    
    client = PrismClient()
    tokens = client.get_bonding_tokens(limit=5)
    
    for token in tokens:
        print(f"${token.symbol} - MC: ${token.market_cap:,.0f} - Holders: {token.holders}")

def example_2_get_graduated_tokens():
    """Example 2: Get recently graduated tokens"""
    print("\n" + "="*50)
    print("Example 2: Get Graduated Tokens")
    print("="*50)
    
    client = PrismClient()
    tokens = client.get_graduated_tokens(limit=5)
    
    for token in tokens:
        print(f"${token.symbol} - MC: ${token.market_cap:,.0f} - Holders: {token.holders}")

def example_3_filter_tokens():
    """Example 3: Filter tokens by criteria"""
    print("\n" + "="*50)
    print("Example 3: Filter Tokens by Criteria")
    print("="*50)
    
    client = PrismClient()
    token_filter = TokenFilter()
    
    tokens = client.get_bonding_tokens(limit=20)
    filtered = [t for t in tokens if token_filter.should_alert(t)]
    
    print(f"Total tokens: {len(tokens)}")
    print(f"Filtered tokens (high-qualified): {len(filtered)}")
    
    for token in filtered[:5]:
        print(f"  ✓ ${token.symbol} - MC: ${token.market_cap:,.0f} - Holders: {token.holders}")

def example_4_format_alerts():
    """Example 4: Format alert messages"""
    print("\n" + "="*50)
    print("Example 4: Format Alert Messages")
    print("="*50)
    
    client = PrismClient()
    alerts = AlertManager()
    
    tokens = client.get_bonding_tokens(limit=1)
    if tokens:
        token = tokens[0]
        
        print("\n📨 New Launch Alert:")
        print(alerts.format_new_launch_alert(token))
        
        print("\n📨 Graduation Alert:")
        print(alerts.format_graduation_alert(token))
        
        print("\n📨 Volume Spike Alert:")
        print(alerts.format_volume_spike_alert(token, volume_increase=250))

def example_5_send_to_office_ui():
    """Example 5: Update Star Office UI Agent Status"""
    print("\n" + "="*50)
    print("Example 5: Update Star Office UI Status")
    print("="*50)
    
    import requests
    
    office_url = os.getenv('OFFICE_UI_URL', 'http://127.0.0.1:18791')
    
    # Simulate trading bot monitoring a token
    payload = {
        'agent': 'trading-bot',
        'state': 'executing',
        'status': 'Monitoring Pump.fun - 5 new tokens detected'
    }
    
    try:
        response = requests.post(f"{office_url}/agent-push", json=payload, timeout=5)
        print(f"✓ Office UI updated: {response.status_code}")
    except Exception as e:
        print(f"✗ Could not reach Office UI: {e}")
        print(f"  (Make sure Star Office UI is running at {office_url})")

def run_all_examples():
    """Run all examples"""
    try:
        example_1_get_bonding_tokens()
        example_2_get_graduated_tokens()
        example_3_filter_tokens()
        example_4_format_alerts()
        example_5_send_to_office_ui()
        
        print("\n" + "="*50)
        print("✓ All examples completed!")
        print("="*50)
        print("\nNext steps:")
        print("1. Copy .env.example to .env")
        print("2. Configure PRISM_URL and alert channels")
        print("3. Run: python alerts.py watch")
        
    except Exception as e:
        print(f"\n✗ Error running examples: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    run_all_examples()
