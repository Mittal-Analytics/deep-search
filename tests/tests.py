import os
import unittest

from src.deep_search import find_blacklist_urls


class DeepSearchTests(unittest.TestCase):
    def test_find_blacklist_urls(self):
        # read CX and GOOGLE_CLOUD_KEY from environment variables
        CX = os.environ["CX"]
        GOOGLE_CLOUD_KEY = os.environ["GOOGLE_CLOUD_KEY"]

        queries = [
            "Avanti Feeds",
            "Acrysil",
            "Bharat Rasayan",
            "Kovai Medical",
            "Meghmani Organics",
        ]
        blacklist = find_blacklist_urls(queries, CX, GOOGLE_CLOUD_KEY)
        self.assertTrue("www.screener.in/company/" in blacklist)


if __name__ == "__main__":
    unittest.main()
