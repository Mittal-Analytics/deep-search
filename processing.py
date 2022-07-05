import json
from urllib.parse import urlparse

with open("data.json", "r") as openFile:
    results = json.load(openFile)

processed = []

for i in results:
    temp = []
    for j in i:
        url = urlparse(j)
        temp.append(
            {
                "domain": url.netloc,
                "path": url.path
            }
        )
    processed.append(temp)

with open("data.json", "w") as writeFile:
    json.dump(processed, writeFile)

