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
generate_tsv(blacklist_urls)

# upload the tsv file to Google Custom Search

# use custom search for better results
custom_search_url = 'url'
results = get_results(custom_search_url)
```

## Algorithm


Library sorts the common urls among different search queries and all their results, required apperance of a url to be excluded is atleast 50%.
