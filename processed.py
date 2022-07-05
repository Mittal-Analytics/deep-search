from itertools import count
import json
import csv

with open("data.json", "r") as openFile:
    data = json.load(openFile)

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

## Initial Remainder

for i in data[0]:
    remainder.append(
        {
            "domain": i["domain"],
            "path": i["path"],
            "seen": 1
        }
    )

## Filtering Happens

for i in data[1:]:
    for j in i:
        filterURL(j)

## Writing to the file

blacklist = []

for i in remainder:
    if i["seen"] > len(data)/2:
        blacklist.append(i["domain"]+i["path"])

with open("blacklist.json", "w") as writeFile:
    json.dump(blacklist, writeFile)

with open("final.tsv", "w") as writeFile:
    tsv_writer = csv.writer(writeFile, delimiter='\t')
    tsv_writer.writerow(["URL", "Label"])
    for i in blacklist:
        tsv_writer.writerow([i+'*', "_exclude_"])