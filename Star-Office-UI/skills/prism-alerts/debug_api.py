#!/usr/bin/env python3
"""Debug script to inspect PRISM API response"""

import requests
import json
from pathlib import Path
from dotenv import load_dotenv
import os

# Load .env
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

BASE_URL = os.getenv('PRISM_URL', 'https://strykr-prism.up.railway.app')

print("\n" + "="*80)
print("🔍 PRISM API DEBUG - INSPECTING API RESPONSE")
print("="*80)

print(f"\n📍 API URL: {BASE_URL}")

# Test bonding endpoint
try:
    print("\n📊 Testing: /crypto/trending/solana/bonding")
    url = f"{BASE_URL}/crypto/trending/solana/bonding"
    response = requests.get(url, timeout=15)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Size: {len(response.text)} bytes")
    
    data = response.json()
    print(f"\n✅ Response JSON:")
    print(json.dumps(data, indent=2)[:1000] + "..." if len(json.dumps(data)) > 1000 else json.dumps(data, indent=2))
    
    # Check structure
    if isinstance(data, dict):
        print(f"\nTopLevel Keys: {list(data.keys())}")
        
        if 'data' in data:
            tokens = data['data']
            print(f"Number of tokens: {len(tokens)}")
            
            if tokens:
                print(f"\n🔍 First token structure:")
                first_token = tokens[0]
                print(json.dumps(first_token, indent=2))
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test graduated endpoint
try:
    print("\n\n📜 Testing: /crypto/trending/solana/graduated")
    url = f"{BASE_URL}/crypto/trending/solana/graduated"
    response = requests.get(url, timeout=15)
    
    print(f"Status Code: {response.status_code}")
    data = response.json()
    
    if isinstance(data, dict) and 'data' in data:
        tokens = data['data']
        print(f"Number of graduated tokens: {len(tokens)}")
        
        if tokens:
            print(f"\n🔍 First graduated token:")
            print(json.dumps(tokens[0], indent=2))

except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*80 + "\n")
