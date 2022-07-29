import csv
import json
import logging
from pathlib import Path
from urllib.parse import urlparse

from googleapiclient.discovery import build

logger = logging.getLogger(__name__)


def _init(key):
    cse = build("customsearch", "v1", developerKey=key)
    return cse


def _longest_common_path(a, b):
    i = j = 0
    while a[i] == b[i]:
        if a[i] == "/":
            j = i
        if i + 1 == len(a) or i + 1 == len(b):
            break
        i += 1
    return a[0 : j + 1]


def _link_sort(link):
    return (link["domain"], link["path"])


def _update_links_list(links, link_list):
    links_index = link_list_index = 0
    while links_index < len(links):

        if (
            links_index + 1 < len(links)
            and links[links_index]["domain"]
            == links[links_index + 1]["domain"]
        ):
            links[links_index + 1]["path"] = _longest_common_path(
                links[links_index]["path"], links[links_index + 1]["path"]
            )
            links_index += 1
            continue

        if link_list_index == len(link_list):
            link_list.append(
                {
                    "domain": links[links_index]["domain"],
                    "path": links[links_index]["path"],
                    "seen": 1,
                }
            )
            links_index += 1
            link_list_index += 1
            continue

        x = links[links_index]
        y = link_list[link_list_index]

        if x["domain"] == y["domain"]:
            link_list[link_list_index]["path"] = _longest_common_path(
                x["path"], y["path"]
            )
            link_list[link_list_index]["seen"] += 1
            links_index += 1
            link_list_index += 1
            continue

        if x["domain"] < y["domain"]:
            link_list.insert(
                link_list_index,
                {"domain": x["domain"], "path": x["path"], "seen": 1},
            )
            links_index += 1

        link_list_index += 1
    return link_list


def _fetch_results(query, service, cx, for_blacklist, cache_version):
    links = []
    for i in range(1, 100, 10):

        logger.info(f"Fetching results for {query}, page {int(i/10 + 1)}...")

        if cache_version != None:
            key = f"cx:{cx}-v:{cache_version}-page:{int(i/10 + 1)}-term:{query}.json"
            cache_f = Path("cache") / key
            if cache_f.exists():
                with open(cache_f, "r") as f:
                    content = f.read()
                res = json.loads(content)
            else:
                res = (
                    service.cse()
                    .list(q=query, cx=cx, start=i)
                    .execute()["items"]
                )
                with open(cache_f, "w") as f:
                    f.write(json.dumps(res))
        else:
            res = (
                service.cse().list(q=query, cx=cx, start=i).execute()["items"]
            )

        if for_blacklist:
            for j in res:
                url = urlparse(j["link"])
                links.append({"domain": url.netloc, "path": url.path})
            links.sort(key=_link_sort)
        else:
            for j in res:
                links.append({"title": j["title"], "link": j["link"]})

    return links


def find_blacklist_urls(queries, cx, key, cache_version):
    service = _init(key)
    link_list = []

    logger.info("Running queries...")
    for query in queries:
        _update_links_list(
            _fetch_results(query, service, cx, True, cache_version), link_list
        )  # True for find_blacklist_urls

    blacklist = []

    for entry in link_list:
        if entry["seen"] >= len(queries) / 1.25:  # 80%
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
    return _fetch_results(
        query, service, cx, False, None
    )  # False for get_results
