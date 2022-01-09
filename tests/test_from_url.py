import unittest

from securitytxt.securitytxt import SecurityTXT


class TestFromURL(unittest.TestCase):
    SECURITYTXT_URLS = ["google.com", "youtube.com", "amazon.com", "yahoo.com", "facebook.com", "reddit.com",
                        "linkedin.com", "walmart.com", "chaturbate.com", "canva.com", "adobe.com", "dropbox.com",
                        "paypal.com", "wordpress.com", "redfin.com", "tradingview.com", "roblox.com", "slack.com",
                        "tumblr.com", "vimeo.com", "github.com", "bbc.com", "wix.com", "grammarly.com", "google.com.hk",
                        "aol.com", "theguardian.com", "expedia.com", "hubspot.com", "nextdoor.com", "shopify.com",
                        "chess.com", "investopedia.com", "amazon.co.uk", "marriott.com", "southwest.com",
                        "creditkarma.com", "okta.com", "bbc.co.uk", "istockphoto.com", "samsclub.com", "techcrunch.com",
                        "trello.com"]
    NONSECURITYTXT_URLS = ["foxnews.com", "bongacams.com", "realtor.com", "hbomax.com", "weather.com", "ca.gov"]

    def test_existing_url(self):
        for url in self.SECURITYTXT_URLS:
            with self.subTest(msg=f"Checking test case {url}"):
                SecurityTXT.from_url(f"http://{url}")

    def test_nonexisting_url(self):
        SecurityTXT.from_url('http://adp.com')
        for url in self.NONSECURITYTXT_URLS:
            with self.subTest(msg=f"Checking test case {url}"):
                self.assertRaises(FileNotFoundError, lambda: SecurityTXT.from_url(f"http://{url}"))

