import unittest
from unittest import TestCase

from src.deep_search import find_blacklist_urls


class SearchTestCase(TestCase):
    def test_get_blacklist_urls(self):
        search_terms = [
            "Avanti Feeds",
            "Acrysil",
            "Bharat Rasayan",
            "Kovai Medical",
            "Meghmani Organics",
        ]
        blacklist_urls = find_blacklist_urls(search_terms)

        self.assertTrue(
            "https://www.moneycontrol.com/stocks/" in blacklist_urls
        )


if __name__ == "__main__":
    unittest.main()
