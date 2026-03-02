"""
Prism Alerts - PRISM API Integration for Pump.fun Token Monitoring

This module provides real-time alerts for Solana token launches, graduations,
and volume spikes using the Strykr PRISM API.

Usage:
    from alerts import PrismClient, AlertManager
    
    client = PrismClient()
    bonding = client.get_bonding_tokens()
"""

__version__ = "1.1.2"
__author__ = "Next Frontier"
__email__ = "contact@nextfrontier.dev"

from alerts import (
    PrismClient,
    AlertManager,
    AlertDatabase,
    TokenFilter,
    PrismAlerts,
    Token
)

__all__ = [
    'PrismClient',
    'AlertManager', 
    'AlertDatabase',
    'TokenFilter',
    'PrismAlerts',
    'Token'
]
