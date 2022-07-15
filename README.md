# deep-search

Library for creating better search results for listed companies. Most of the results in Google search are currently for finance portals. This uses Google's custom search to exclude finance portals.


## Usage

```python
from deep_search import find_blacklist_urls, generate_tsv, get_results

# generate list of common urls
search_terms = [
    "Avanti Feeds", 
    "Acrysil", 
    "Bharat Rasayan", 
    "Kovai Medical", 
    "Meghmani Organics"
]
blacklist_urls = find_blacklist_urls(search_terms)
generate_tsv("custom-search.tsv", blacklist_urls)

# upload the tsv file to Google Custom Search

# use custom search for better results
custom_search_url = 'url'
results = get_results(custom_search_url)
```

## Algorithm

The blacklist_urls are found by finding common urls across given search terms.

- save first 100 results for each search term
- find common urls in at-least 80% of the search terms (4 companies if we give 5 names)
- the common url is NOT the root-url
- the common url is a repeated pattern for different company names
- concept of "holes" might be useful for this: https://github.com/paulsmith/templatemaker