import csv
import json
from distutils.command.config import config
from pathlib import Path
from urllib.parse import urlparse

from dotenv import dotenv_values
from googleapiclient.discovery import build

CONFIG = dotenv_values(".env")


def _get_longest_common_path(a, b):
    i = 0
    while a[i] == b[i]:
        if i + 1 == len(a) or i + 1 == len(b):
            break
        i += 1
    while a[i] != "/":
        i -= 1
    return a[0 : i + 1]


def _filter_url(remainder, url):
    flag1 = 1
    flag2 = 1

    for i in remainder:
        if i["domain"] == url["domain"]:
            flag1 = 0
            if i["path"] in url["path"]:
                flag2 = 0
                i["seen"] += 1
                break
            else:
                ci = i
    if flag1:
        remainder.append(
            {"domain": url["domain"], "path": url["path"], "seen": 1}
        )
    elif flag2:
        remainder.append(
            {
                "domain": url["domain"],
                "path": _get_longest_common_path(ci["path"], url["path"]),
                "seen": ci["seen"] + 1,
            }
        )
    return remainder


def _find_blacklist_urls(data):
    remainder = []
    for i in data:
        _filter_url(remainder, i)

    blacklist_urls = []
    for i in remainder:
        if i["seen"] > len(data) / 200:
            blacklist_urls.append(i["domain"] + i["path"])
    return blacklist_urls


def _fetch_results(term, start):
    CX = config["CX"]
    V = config["V"]
    DEV_KEY = config["DEV_KEY"]

    key = f"cx:{CX}-v:{V}-page:{start}-term:{term}.json"
    cache_f = Path("cache") / key
    if cache_f.exists():
        with open(cache_f, "r") as f:
            content = f.read()
        data = json.loads(content)
    else:
        service = build(
            "customsearch",
            "v1",
            developerKey=DEV_KEY,
        )
        data = service.cse().list(q=term, cx=CX, start=start).execute()
        with open(cache_f, "w") as f:
            f.write(json.dumps(data))
    return data


def find_blacklist_urls(search_terms):
    results = []
    for term in search_terms:
        for i in range(1, 100, 10):
            res = _fetch_results(term, i)
        if "items" in res:
            for j in res["items"]:
                results.append(j["link"])
        else:
            break

    data = []
    for i in results:
        url = urlparse(i)
        data.append({"domain": url.netloc, "path": url.path})

    blacklist_urls = _find_blacklist_urls(data)
    return blacklist_urls


def generate_tsv(filename, blacklist_urls):
    with open(filename, "w") as writeFile:
        tsv_writer = csv.writer(writeFile, delimiter="\t")
        tsv_writer.writerow(["URL", "Label"])
        for i in blacklist_urls:
            tsv_writer.writerow([i + "*", "_exclude_"])
