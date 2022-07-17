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

def _longest_common_path(a, b):
    i = 0
    while a[i] == b[i]:
        if i + 1 == len(a) or i + 1 == len(b):
            break
        i += 1
    while a[i] != '/':
        i -= 1
    return a[0:i+1]


def _update_list(links, link_list):
    for link in links:
        match_not_found = True
        for entry in link_list:
            if link["domain"] == entry["domain"]:
                match_not_found = False
                a = link["path"]
                b = entry["path"]
                if a in b or b in a:
                    entry["path"] = _longest_common_path(a, b)
                    entry["seen"] += 1
        if match_not_found:
            link_list.append({
                "domain": link["domain"],
                "path": link["path"],
                "seen": 1
            })
    #Pending...
    return link_list

def _fetch_results(query, service, cx, for_blacklist):
    links = []
    for i in range(1,50,10):
        res = service.cse().list(q=query, cx=cx, start=i).execute()["items"]
        if for_blacklist:
            for j in res:
                url = urlparse(j["link"])
                links.append({
                    "domain": url.netloc,
                    "path": url.path
                })
        else:
            for j in res:
                links.append({
                    "title": j["title"],
                    "link": j["link"]
                })

    return links

def find_blacklist_urls(queries, cx, key):
    service = _init(key)
    link_list = []

    for query in queries:
        link_list = _update_list(_fetch_results(query, service, cx, True), link_list) #True for find_blacklist_urls

    blacklist = []

    for entry in link_list:
        if entry["seen"] >= len(queries)/1.25: #80%
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
    return _fetch_results(query, service, cx, False) #False for get_results


print(find_blacklist_urls(["Avanti Feeds", "Pix Transmission", "Kovai Medical", "Rossell India", "Acrysil"], "cea393e795c307f0f", "AIzaSyDjL9Kcfl6O2Zvl_2alvqXSPsAnba0hEhw"))