#!/usr/bin/env python3
"""
Prism Alerts Unit Tests
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import json
from datetime import datetime
from alerts import Token, PrismClient, TokenFilter, AlertDatabase, AlertManager

class TestToken(unittest.TestCase):
    """Test Token dataclass"""
    
    def test_token_creation(self):
        token = Token(
            token_id="CA123",
            symbol="TEST",
            name="Test Token",
            market_cap=10000,
            holders=50,
            bonding_progress=25.0,
            created_at="2024-01-01T00:00:00",
            url="https://pump.fun/CA123"
        )
        
        self.assertEqual(token.symbol, "TEST")
        self.assertEqual(token.market_cap, 10000)
        self.assertEqual(token.status, "bonding")

class TestTokenFilter(unittest.TestCase):
    """Test TokenFilter logic"""
    
    def setUp(self):
        self.filter = TokenFilter()
        self.token = Token(
            token_id="CA123",
            symbol="TEST",
            name="Test Token",
            market_cap=10000,
            holders=50,
            bonding_progress=25.0,
            created_at="2024-01-01",
            url="https://pump.fun/CA123"
        )
    
    def test_should_alert_valid_token(self):
        """Valid token should pass filter"""
        result = self.filter.should_alert(self.token)
        self.assertTrue(result)
    
    def test_should_alert_low_market_cap(self):
        """Token with low market cap should fail"""
        self.token.market_cap = 1000
        result = self.filter.should_alert(self.token)
        self.assertFalse(result)
    
    def test_should_alert_high_market_cap(self):
        """Token with market cap too high should fail"""
        self.token.market_cap = 500000
        result = self.filter.should_alert(self.token)
        self.assertFalse(result)
    
    def test_should_alert_low_holders(self):
        """Token with few holders should fail"""
        self.token.holders = 5
        result = self.filter.should_alert(self.token)
        self.assertFalse(result)
    
    def test_should_alert_low_bonding_progress(self):
        """Token with low bonding progress should fail"""
        self.token.bonding_progress = 5.0
        result = self.filter.should_alert(self.token)
        self.assertFalse(result)

class TestAlertDatabase(unittest.TestCase):
    """Test AlertDatabase deduplication"""
    
    def setUp(self):
        self.db = AlertDatabase(':memory:')  # Use in-memory DB for tests
    
    def test_record_alert(self):
        """Should record an alert"""
        self.db.record_alert("CA123", "new_launch")
        self.assertTrue(self.db.has_alert("CA123", "new_launch", cooldown_minutes=60))
    
    def test_cooldown_expiry(self):
        """Alert should not be in cooldown after expiry"""
        self.db.record_alert("CA123", "new_launch")
        # Should be in cooldown with 60 min window, not with 0 min
        self.assertFalse(self.db.has_alert("CA123", "new_launch", cooldown_minutes=0))

class TestAlertManager(unittest.TestCase):
    """Test AlertManager formatting"""
    
    def setUp(self):
        self.manager = AlertManager()
        self.token = Token(
            token_id="CA123",
            symbol="DOGE",
            name="Dogecoin Clone",
            market_cap=42069,
            holders=234,
            bonding_progress=67.5,
            created_at="2024-01-01T12:34:56",
            url="https://pump.fun/CA123"
        )
    
    def test_format_new_launch_alert(self):
        """Should format new launch alert"""
        message = self.manager.format_new_launch_alert(self.token)
        self.assertIn("🚀", message)
        self.assertIn("$DOGE", message)
        self.assertIn("42069", message)
    
    def test_format_graduation_alert(self):
        """Should format graduation alert"""
        message = self.manager.format_graduation_alert(self.token)
        self.assertIn("🎓", message)
        self.assertIn("$DOGE", message)
    
    def test_format_volume_spike_alert(self):
        """Should format volume spike alert"""
        message = self.manager.format_volume_spike_alert(self.token, 250)
        self.assertIn("📈", message)
        self.assertIn("250", message)

class TestPrismClient(unittest.TestCase):
    """Test PRISM API Client"""
    
    @patch('requests.Session.get')
    def test_get_bonding_tokens(self, mock_get):
        """Should fetch bonding tokens from API"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'data': [
                {
                    'token_id': 'CA123',
                    'symbol': 'TEST',
                    'name': 'Test Token',
                    'market_cap': 10000,
                    'holders': 50,
                    'bonding_progress': 25.0,
                    'created_at': '2024-01-01',
                    'url': 'https://pump.fun/CA123'
                }
            ]
        }
        mock_get.return_value = mock_response
        
        client = PrismClient()
        tokens = client.get_bonding_tokens()
        
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].symbol, "TEST")
    
    @patch('requests.Session.get')
    def test_get_bonding_tokens_api_error(self, mock_get):
        """Should handle API errors gracefully"""
        mock_get.side_effect = Exception("Connection error")
        
        client = PrismClient()
        tokens = client.get_bonding_tokens()
        
        self.assertEqual(len(tokens), 0)

def suite():
    """Create test suite"""
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestToken))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestTokenFilter))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestAlertDatabase))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestAlertManager))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestPrismClient))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
