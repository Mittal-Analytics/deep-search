import json

with open("data.json", "r") as openFile:
    results = json.load(openFile)

processed = []

for i in results:
    temp = []
    for j in i:
        for k in range(8, len(j), 1):
            if j[k] == '/':
                domainEnd = k
                break
        temp.append(
            {
                "domain": j[8:domainEnd],
                "path": j[domainEnd:]
            }
        )
    processed.append(temp)

with open("data.json", "w") as writeFile:
    json.dump(processed, writeFile)

