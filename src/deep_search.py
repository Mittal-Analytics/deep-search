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
    i,j = 0
    while a[i] == b[i]:
        if i + 1 == len(a) or i + 1 == len(b):
            break
        if a[i] == '/': j = i
        i += 1
    return a[0:j+1]

def _link_sort(link):
    return (link["domain"], link["path"])

def _update_list(links, link_list):
    i = 0
    j = 0
    while i < len(links):

        if i+1 < len(links) and links[i]["domain"] == links[i+1]["domain"]:
            links[i+1]["path"] = _longest_common_path(links[i]["path"], links[i+1]["path"])
            i += 1
            continue

        if j == len(link_list):
            link_list.append({
                "domain": links[i]["domain"],
                "path": links[i]["path"],
                "seen": 1
            })
            i += 1
            j += 1
            continue

        x = links[i]
        y = link_list[j]

        if x["domain"] == y["domain"]:
            link_list[j]["path"] = _longest_common_path(x["path"], y["path"])
            link_list[j]["seen"] += 1
            i += 1
            j += 1
            continue

        if x["domain"] < y["domain"]:
            link_list.insert(j, {
                "domain": x["domain"],
                "path": x["path"],
                "seen": 1
            })
            i += 1

        j += 1
    return link_list

def _fetch_results(query, service, cx, for_blacklist):
    links = []
    for i in range(1,100,10):
        res = service.cse().list(q=query, cx=cx, start=i).execute()["items"]
        if for_blacklist:
            for j in res:
                url = urlparse(j["link"])
                links.append({
                    "domain": url.netloc,
                    "path": url.path
                })
            links.sort(key=_link_sort)
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
        white_link = urlparse(white_link).netloc + urlparse(white_link).path
        for black_link in blacklist:
            if white_link in black_link or black_link in white_link:
                blacklist.remove(black_link)
    with open(file_name, "w") as file:
        tsv_writer = csv.writer(file, delimiter="\t")
        tsv_writer.writerow(["URL", "Label"])
        for link in blacklist:
            tsv_writer.writerow([link + "*", "_exclude_"])

def get_results(query, cx, key):
    service = _init(key)
    return _fetch_results(query, service, cx, False) #False for get_results