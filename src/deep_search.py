import csv
from googleapiclient.discovery import build
from urllib.parse import urlparse

def _init(key):
    cse = build(
        "customsearch",
        "v1",
        developerKey = key
    )
    return cse

def _update_list(links, link_list):
    #Pending...
    return link_list

def _fetch_results(query, service, cx, type):
    links = []
    for i in range(1,100,10):
        res = service.cse().list(q=query, cx=cx, start=i).execute()["items"]
        if type == "fbu":
            for j in res:
                url = urlparse(j["link"])
                links.append({
                    "domain": url.netloc,
                    "path": url.path
                })
        elif type == "gr":
            for j in res:
                links.append({
                    "title": j["title"],
                    "link": j["link"]
                })

    return links

def find_blacklist_urls(queries, cx, key):
    service = _init(key)

    for query in queries:
        link_list = _update_list(_fetch_results(query, service, cx, "fbu"), link_list) #fbu for find_blacklist_urls

    blacklist = []

    for entry in link_list:
        if entry["seen"] > len(queries)/1.25: #80%
            blacklist.append(entry["domain"] + entry["path"])

    return blacklist

def generate_tsv(file_name, blacklist, whitelist):
    for white_link in whitelist:
        for black_link in blacklist:
            if white_link in black_link:
                blacklist.remove(black_link)
    with open(file_name, "w") as file:
        tsv_writer = csv.writer(file, delimiter="\t")
        tsv_writer.writerow(["URL", "Label"])
        for link in blacklist:
            tsv_writer.writerow([link + "*", "_exclude_"])

def get_results(query, cx, key):
    service = _init(key)
    return _fetch_results(query, service, cx, "gr") #gr for get_results


find_blacklist_urls(["Avanti Feeds", "Reliance Industries"], "cea393e795c307f0f", "AIzaSyDjL9Kcfl6O2Zvl_2alvqXSPsAnba0hEhw")