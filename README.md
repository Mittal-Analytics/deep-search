# deep-search

Library for creating better search results for listed companies. Most of the results in Google search are currently for finance portals. This uses Google's custom search to exclude finance portals.


## Usage

Add `GOOGLE_CLOUD_KEY` and `CX` to your environment variables.

```bash
# generate custom search API credentials at:
# https://console.cloud.google.com/apis/credentials
export GOOGLE_CLOUD_KEY="key-generated-from-console"

# create custom search url
# https://programmablesearchengine.google.com/cse/all
# paste "Search Engine ID" here
export CX="search-engine-id"
```

Use the API to generate tsv.

```python
import os
from deep_search import find_blacklist_urls, generate_tsv, get_results

# read CX and GOOGLE_CLOUD_KEY from environment variables
CX = os.environ['CX']
GOOGLE_CLOUD_KEY = os.environ['GOOGLE_CLOUD_KEY']

# generate list of common urls
search_terms = [
    "Avanti Feeds", 
    "Acrysil", 
    "Bharat Rasayan", 
    "Kovai Medical", 
    "Meghmani Organics"
]
blacklist_urls = find_blacklist_urls(
    search_terms,
    CX,
    GOOGLE_CLOUD_KEY,
    # providing cache_key will cache the search results from Google
    cache_key="v1",
)
# urls which should be ignored from blacklist
whitelist_urls ['https://forbes.com']
generate_tsv("custom-search.tsv", blacklist_urls, whitelist_urls)

# upload the tsv file to Google Custom Search

# use custom search for better results
search_term = "Avanti Feeds"
results = get_results(search_term, cx, key)
```

## Algorithm

The blacklist_urls are found by finding common urls across given search terms.

- save first 100 results for each search term
- find common urls in at-least 80% of the search terms (4 companies if we give 5 names)
- the common url is NOT the root-url
- the common url is a repeated pattern for different company names
- concept of "holes" might be useful for this: https://github.com/paulsmith/templatemaker

The script should try to hit as few urls as possible. Caching search results might be a good idea.


## Development

Running tests:

```
python -m unittest
```