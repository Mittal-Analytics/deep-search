# deep-search

This is a python library for generating a list of commons urls among different search results with the use of google's custom search api. The primary use would be to generate a tsv file through one of its function and upload it on google's programmable search engine to refine the search results.

For example, it could be used to eliminate finance portals when we search for a listed company and only see the relevant information.

## Usage

Install the library (only available for testing currently):

```bash
pip install -i https://test.pypi.org/simple/ --no-deps deep-search
```

Note: Please install the dependencies seprately for proper behaviour as they are not available in testing mode.

You need to get two things now:

1. GOOGLE_CLOUD_KEY/
   This is the Custom Search API credential and can be generated through this link:
   https://console.cloud.google.com/apis/credentials
2. CX/
   This is the id of your Custom Search Engine and can be generated through this link:
   https://programmablesearchengine.google.com/cse/all

You are now good to go, here is a demo implementation:

```python
import os
from deep_search.deep_search import find_blacklist_urls, generate_tsv, get_results

# We recommend using environment variables to keep these credentials secure, read GOOGLE_CLOUD_KEY, CX and CACHE_VERSION from the environment variables.
CX = os.environ['CX']
GOOGLE_CLOUD_KEY = os.environ['GOOGLE_CLOUD_KEY']
CACHE_VERSION = os.environ['CACHE_VERSION']
# Specify CACHE_VERSION as None for no caching.

# Define the terms you want to generate the list of common urls for
search_terms = [
    "Avanti Feeds",
    "Acrysil",
    "Bharat Rasayan",
    "Kovai Medical",
    "Meghmani Organics"
]

# Plug everything in this function, returns a list of common urls.
blacklist_urls = find_blacklist_urls(
    search_terms,
    CX,
    GOOGLE_CLOUD_KEY,
    CACHE_VERSION,
)

# Specify the urls that you do not want to be included in the final tsv file.
whitelist_urls ['https://www.forbes.com/']

# Give a name to your tsv file and plug the variables, generates a tsv file.
generate_tsv("custom-search.tsv", blacklist_urls, whitelist_urls)

# This is where you upload the generated tsv to your Custom Search Engine at https://programmablesearchengine.google.com/cse/all (manually).

# Use the given function to fetch refined results, returns a json list with title and link property.
search_term = "Avanti Feeds"
results = get_results(search_term, cx, key)
```

## Development

Setting up dev environment:

```bash
# create and activate virtual env
python3 -m venv .venv
source .venv/bin/activate

# install requirements
pip install '.[dev]'

# provide credentials
cp .envrc.sample .envrc
# edit and update the credentials in .env file
vi .envrc

# running tests
python -m unittest
```
