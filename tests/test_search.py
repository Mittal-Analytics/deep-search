import unittest

from final import get_blacklist

class SearchTestCases(unittest.TestCase):
    def test_search(self):
        blacklist = get_blacklist()
        expected = []
        self.maxDiff = None
        self.assertEqual(blacklist, expected)

if __name__ == "__main__":
    unittest.main()