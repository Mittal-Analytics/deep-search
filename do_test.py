import json

data = json.load(open("data.json"))

def get_exclusions():

    remainder = []

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

    for i in data:
        filter_url(i)

    blacklist = []

    for i in remainder:
        if i["seen"] > len(data)/200:
            blacklist.append(i["domain"]+i["path"])

    print(blacklist)
    return blacklist

get_exclusions()