import json
from urllib.parse import urlparse
from googleapiclient.discovery import build

companies = ["Avanti Feeds", 
             "Acrysil", 
             "Bharat Rasayan", 
             "Kovai Medical", 
             "Meghmani Organics"]
remainder = []
blacklist = []

def setup():

    results = []
    data = []

    service = build(
        "customsearch", "v1", developerKey="AIzaSyDjL9Kcfl6O2Zvl_2alvqXSPsAnba0hEhw"
    )

    for company in companies:

        for i in range(1, 100, 10):
            res = (
                service.cse()
                .list(
                    q=company,
                    cx="cea393e795c307f0f",
                    start = i
                )
                .execute()
            )

            if "items" in res:
                for j in res["items"]:
                    results.append(j["link"])
            else: break

    for i in results:
        url = urlparse(i)
        data.append(
            {
                "domain": url.netloc,
                "path": url.path
            }
        )
    
    return data
        
## Execution starts here
data = setup()

f = open("data.json", "w")
json.dump(data, f)