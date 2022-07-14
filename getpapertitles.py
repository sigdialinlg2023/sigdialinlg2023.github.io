import json

with open("sitedata/papers.json") as f:
    papers = json.load(f)
titles = [x["title"] for x in papers.values()]
with open("titles.txt", "w") as f:
    for title in titles:
        f.write(title + "\n")
