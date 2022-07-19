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
        blacklist = find_blacklist_urls(queries, "cx", "key")
        #cx - custom search engine identity should be for the engine with no alterations
        found = False
        for link in blacklist:
            if "www.moneycontrol.com/" in link:
                found = True
                break
        self.assertTrue(found)

    def test_get_results(self):
        query = "Avanti Feeds"
        results = get_results(query, "cx", "key")
        #cx - custom search engine identity should be for the engine after alterations
        found = False
        for link in results:
            if "www.indiankanoon.org/" in link["link"]:
                found = True
                break
        self.assertTrue(found)

if __name__ == "__main__":
    unittest.main()