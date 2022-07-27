import logging
import os
import unittest

from src.deep_search import find_blacklist_urls

logging.basicConfig(level=logging.INFO)


class DeepSearchTests(unittest.TestCase):
    def test_find_blacklist_urls(self):

        # Read CX and GOOGLE_CLOUD_KEY from environment variables
        CX = os.environ["CX"]
        GOOGLE_CLOUD_KEY = os.environ["GOOGLE_CLOUD_KEY"]
        CACHE_VERSION = os.environ["CACHE_VERSION"]

        queries = [
            "Avanti Feeds",
            "Acrysil",
            "Bharat Rasayan",
            "Kovai Medical",
            "Meghmani Organics",
        ]

        blacklist = find_blacklist_urls(
            queries, CX, GOOGLE_CLOUD_KEY, CACHE_VERSION
        )
        self.assertTrue("www.screener.in/company/" in blacklist)


if __name__ == "__main__":
    unittest.main()
