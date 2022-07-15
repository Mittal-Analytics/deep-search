# deep-search

Library for creating better search results for listed companies. Most of the results in Google search are currently for finance portals. This uses Google's custom search to exclude finance portals.


## Usage

```python
from deep_search import build_tsv, get_results

# generate tsv file for uploading on Google Custom Search
build_tsv('custom-search.tsv')

# upload the tsv file to Google Custom Search

# use custom search for better results
custom_search_url = 'url'
results = get_results(custom_search_url)
```