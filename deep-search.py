import csv
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

def longest_common_path(a, b):
    i = 0
    while a[i] == b[i]:
        if i+1 == len(a) or i+1 == len(b):
            break
        i+=1
    while a[i] != '/':
        i-=1
    return a[0:i+1]

def filter_url(url):
    is_domain = 1
    is_path = 1

    for i in remainder:
        if i["domain"] == url["domain"]:
            is_domain = 0
            if i["path"] in url["path"]:
                is_path = 0
                i["seen"] += 1
                break
            else: ci = i
    if is_domain:
        remainder.append({
            "domain": url["domain"],
            "path": url["path"],
            "seen": 1
        })
    elif is_path:
        remainder.append({
            "domain": url["domain"],
            "path": longest_common_path(ci["path"], url["path"]),
            "seen": ci["seen"] + 1
        })
        
## Execution starts here
data = setup()
for i in data:
    filter_url(i)

## Writing to the file
for i in remainder:
    if i["seen"] > len(data)/(2*100):
        blacklist.append(i["domain"]+i["path"])
        
with open("final.tsv", "w") as writeFile:
    tsv_writer = csv.writer(writeFile, delimiter='\t')
    tsv_writer.writerow(["URL", "Label"])
    for i in blacklist:
        tsv_writer.writerow([i+'*', "_exclude_"])