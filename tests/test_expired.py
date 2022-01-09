import unittest
from datetime import datetime, timedelta, timezone

from securitytxt.securitytxt import SecurityTXT


class TestExpired(unittest.TestCase):

    def test_future_date(self):
        securitytxt = SecurityTXT()
        securitytxt.expires = datetime.now() + timedelta(days=5)
        self.assertFalse(securitytxt.expired)

    def test_past_date(self):
        securitytxt = SecurityTXT()
        securitytxt.expires = datetime.now() + timedelta(days=-5)
        self.assertTrue(securitytxt.expired)