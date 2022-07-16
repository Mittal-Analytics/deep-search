import unittest
from src.deep_search import find_blacklist_urls, get_results

class deep_search_tests(unittest.TestCase):
    def test_find_blacklist_urls(self):
        queries = [
            "Avanti Feeds",
            "Acrysil",
            "Bharat Rasayan",
            "Kovai Medical",
            "Meghmani Organics",
        ]
        blacklist = find_blacklist_urls(queries, "cea393e795c307f0f", "AIzaSyDjL9Kcfl6O2Zvl_2alvqXSPsAnba0hEhw")
        self.assertTrue("www.moneycontrol.com/?" in blacklist)

    def test_get_results(self):
        query = "Avanti Feeds"
        results = get_results(query, "cea393e795c307f0f", "AIzaSyDjL9Kcfl6O2Zvl_2alvqXSPsAnba0hEhw")
        self.assertTrue("www.indiankanoon.org/?" in results)

if __name__ == "__main__":
    unittest.main()