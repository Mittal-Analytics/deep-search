import logging
import os
import unittest

from src.deep_search.deep_search import (
    _longest_common_path,
    _update_links_list,
    find_blacklist_urls,
    get_results,
)

logging.basicConfig(level=logging.INFO)


class DeepSearchTests(unittest.TestCase):
    def test_find_blacklist_urls(self):

        # Read CX and GOOGLE_CLOUD_KEY from environment variables
        CX = os.environ["CX"]
        GOOGLE_CLOUD_KEY = os.environ["GOOGLE_CLOUD_KEY"]
        CACHE_VERSION = os.environ["CACHE_VERSION"]

        queries = [
            "Avanti Feeds",
            "Carysil",
            "Bharat Rasayan",
            "Kovai Medical",
            "Meghmani Organics",
        ]

        blacklist = find_blacklist_urls(queries, CX, GOOGLE_CLOUD_KEY, CACHE_VERSION)
        self.assertTrue("www.screener.in/company/" in blacklist)

    def test_longest_common_path(self):
        path = _longest_common_path("/abc/xyz/ijk/", "/abc/xyz/ilu")
        self.assertEqual(path, "/abc/xyz/")

    def test_update_links_list(self):
        links_list = [
            {"domain": "www.screener.com", "path": "/company/", "seen": 1},
            {"domain": "www.trendlyne.com", "path": "/equity/", "seen": 1},
        ]
        links = [
            {"domain": "www.screener.com", "path": "/company/itc/"},
            {"domain": "www.trendlyne.com", "path": "/"},
        ]
        _update_links_list(links, links_list)
        expected = [
            {"domain": "www.screener.com", "path": "/company/", "seen": 2},
            {"domain": "www.trendlyne.com", "path": "/", "seen": 2},
        ]
        self.assertEqual(expected, links_list)

    def test_get_results(self):
        CX = os.environ["CX"]
        GOOGLE_CLOUD_KEY = os.environ["GOOGLE_CLOUD_KEY"]
        results = get_results("Carysil", CX, GOOGLE_CLOUD_KEY)
        self.assertTrue(
            {
                "title": "Carysil Ltd financial results and price chart - Screener",
                "link": "https://www.screener.in/company/CARYSIL/consolidated/",
            }
            not in results
        )


if __name__ == "__main__":
    unittest.main()
