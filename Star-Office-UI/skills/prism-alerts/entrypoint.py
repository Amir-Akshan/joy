#!/usr/bin/env python3
"""
Prism Alerts - Docker/Container Entry Point
Allows running alerts in containerized environment
"""

import os
import sys
import logging
from pathlib import Path

# Setup logging for container environment
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point for container execution"""
    
    # Import after module is ready
    from alerts import PrismAlerts
    
    logger.info("Prism Alerts Container Started")
    
    # Get command from environment or argument
    command = os.getenv('COMMAND', sys.argv[1] if len(sys.argv) > 1 else 'watch')
    
    logger.info(f"Executing command: {command}")
    
    try:
        alerts = PrismAlerts()
        
        if command == 'bonding':
            tokens = alerts.client.get_bonding_tokens()
            print(f"Found {len(tokens)} tokens on bonding curve")
            sys.exit(0)
        
        elif command == 'graduated':
            tokens = alerts.client.get_graduated_tokens()
            print(f"Found {len(tokens)} graduated tokens")
            sys.exit(0)
        
        elif command == 'watch':
            logger.info("Starting watch mode...")
            alerts.watch_tokens()
        
        elif command == 'trending':
            bonding = alerts.client.get_bonding_tokens()
            graduated = alerts.client.get_graduated_tokens()
            print(f"Trending: {len(bonding)} bonding + {len(graduated)} graduated")
            sys.exit(0)
        
        else:
            logger.error(f"Unknown command: {command}")
            sys.exit(1)
    
    except KeyboardInterrupt:
        logger.info("Shutdown requested")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
