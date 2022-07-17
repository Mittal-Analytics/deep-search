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
        found = False
        for link in blacklist:
            if "www.moneycontrol.com/" in link:
                found = True
                break
        self.assertTrue(found)

    def test_get_results(self):
        query = "Avanti Feeds"
        results = get_results(query, "cea393e795c307f0f", "AIzaSyDjL9Kcfl6O2Zvl_2alvqXSPsAnba0hEhw")
        found = False
        for link in results:
            if "www.indiankanoon.org/" in link["link"]:
                found = True
                break
        self.assertTrue(found)

if __name__ == "__main__":
    unittest.main()