import unittest
from supporting_url_finder.linkanalyzer import LinkFinder

class TestUrlParser(unittest.TestCase):

    def setUp(self):
        self.google = LinkFinder("google.com")
        self.google.base_url = "google.com"

        self.twitter = LinkFinder("twitter.com")
        self.twitter.base_url = "twitter.com"

        self.covenanteyes = LinkFinder("covenanteyes.com")
        self.covenanteyes.base_url = "covenanteyes.com"

        self.justinsiebert = LinkFinder("justinsiebert.com")
        self.justinsiebert.base_url = "justinsiebert.com"

    def test_normalize_url(self):
        self.assertEqual(self.google.normalize_url("/test"), "google.com/test")
        self.assertEqual(self.google.normalize_url("//google.com/sub"), "http://google.com/sub")
        self.assertEqual(self.google.normalize_url("/test"), "google.com/test")

        self.assertEqual(self.twitter.normalize_url("/tweet"), "twitter.com/tweet")

        self.assertEqual(self.justinsiebert.normalize_url("#about"), "justinsiebert.com/#about")

    def test_junk_url(self):
        self.assertTrue(self.covenanteyes.junk_url("mailto:support@covenanteyes.com"))
        self.assertTrue(self.covenanteyes.junk_url("tel:877-479-1119"))
        self.assertFalse(self.covenanteyes.junk_url("covenanteyes.com/myaccount"))
