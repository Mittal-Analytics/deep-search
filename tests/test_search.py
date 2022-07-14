import unittest
from do_test import get_exclusions

class SearchTestCases(unittest.TestCase):
    def test_search(self):
        blacklist = get_exclusions()
        expected = ['www.tcs.com/', 'sunpharma.com/', 'en.wikipedia.org/wiki/', 'twitter.com/', 'www.hul.co.in/', 'www.unilever.com/', 'www.morningstar.com/stocks/xnse/', 'www.weforum.org/organizations/', 'www.unglobalcompact.org/what-is-gc/participants/', 'stocktwits.com/symbol/', 'www.wsj.com/market-data/quotes/in/', 'www.cnbctv18.com/', 'www.pidilite.com/', 'www.investing.com/equities/', 'patents.justia.com/assignee/', 'www.morningstar.in/stocks/', 'www.gurufocus.com/term/', 'www.facebook.com/', 'moovitapp.com/index/en/', 'indiankanoon.org/doc/', 'uk.linkedin.com/in/', 'www.livemint.com/', 'in.indeed.com/cmp/', 'apps.apple.com/', 'companiesmarketcap.com/', 'www.instagram.com/', 'play.google.com/store/apps/', 'indianexpress.com/article/', 'www.zoominfo.com/c/', 'www.forbesindia.com/article/', 'markets.businessinsider.com/news/', 'www.youtube.com/']
        self.maxDiff = None
        self.assertEqual(blacklist, expected)

if __name__ == "__main__":
    unittest.main()