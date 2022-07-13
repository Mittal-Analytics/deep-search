import csv
from urllib.parse import urlparse
from googleapiclient.discovery import build

companies = ["Avanti Feeds", 
             "Acrysil", 
             "Bharat Rasayan", 
             "Kovai Medical", 
             "Meghmani Organics"]

results = []

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

data = []

for i in results:
    url = urlparse(i)
    data.append(
        {
            "domain": url.netloc,
            "path": url.path
        }
    )

############

## The comparison happens now

remainder = []

## Longest common path

def longestCommonPath(a, b):
    i = 0
    while a[i] == b[i]:
        if i+1 == len(a) or i+1 == len(b):
            break
        i+=1
    while a[i] != '/':
        i-=1
    return a[0:i+1]

## Filter URL

def filterURL(url):
    flag1 = 1
    flag2 = 1

    for i in remainder:
        if i["domain"] == url["domain"]:
            flag1 = 0
            if i["path"] in url["path"]:
                flag2 = 0
                i["seen"] += 1
                break
            else: ci = i
    if flag1:
        remainder.append({
            "domain": url["domain"],
            "path": url["path"],
            "seen": 1
        })
    elif flag2:
        remainder.append({
            "domain": url["domain"],
            "path": longestCommonPath(ci["path"], url["path"]),
            "seen": ci["seen"] + 1
        })

## Filtering Happens

for i in data:
    filterURL(i)

## Writing to the file

blacklist = []

for i in remainder:
    if i["seen"] > len(data)/200:
        blacklist.append(i["domain"]+i["path"])
        
with open("final.tsv", "w") as writeFile:
    tsv_writer = csv.writer(writeFile, delimiter='\t')
    tsv_writer.writerow(["URL", "Label"])
    for i in blacklist:
        tsv_writer.writerow([i+'*', "_exclude_"])