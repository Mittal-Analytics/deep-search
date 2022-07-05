from googleapiclient.discovery import build
import json

companies = ["Avanti Feeds", 
             "Acrysil", 
             "Bharat Rasayan", 
             "Kovai Medical", 
             "Meghmani Organics"]

results = []

service = build(
    "customsearch", "v1", developerKey="AIzaSyDjL9Kcfl6O2Zvl_2alvqXSPsAnba0hEhw"
)

for a in companies:
    tot_res = []

    for i in range(1, 100, 10):
        res = (
            service.cse()
            .list(
                q=a,
                cx="cea393e795c307f0f",
                start = i
            )
            .execute()
        )

        for j in res["items"]:
            tot_res.append(j["link"])

    results.append(tot_res)

with open("data.json", "w") as jsonFile:
    json.dump(results, jsonFile)
    