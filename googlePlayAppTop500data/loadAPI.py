import json
import requests

# access_token = "dae45e93d4c21f3121b2200df98b137ece874df8"
access_token = "786a2246f89ddcb2940edf51a73e4c2f80f09918"
# access_token = "3ed83d4ee417e76b4b1d7b3d5cccbeea60ccbcf8"


def getAPI(package_name, access_token):
    queryLink = 'https://data.42matters.com/api/v2.0/android/apps/lookup.json?p=' + package_name + '&access_token=' + access_token
    queryResult = requests.get(queryLink)
    if queryResult.text:
        item = json.loads(queryResult.text)
        info = {
            "title": item.get("title"),
            "package_name": item.get("package_name"),
            "rating": item.get("rating"),
            "downloads": item.get("downloads"),
            "category": item.get("category"),
            "short_desc": item.get("short_desc"),
            "description": item.get("description"),
        }
        return info


with open("./data/nonfree app top540.txt") as f_read:
    with open("./data/nonfreeTop450Info.txt", 'a', encoding="utf-8") as f_write:
        lines = f_read.readlines()
        newLines = []
        for line in lines:
            line = line.strip()
            newLines.append(line)

        for line in newLines[465:540]:
            package_name = eval(line).get("package")

            info = getAPI(package_name, access_token)
            print(info)
            f_write.write(str(info) + "\n")
