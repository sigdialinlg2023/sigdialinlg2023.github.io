import openreview
import requests
import json
import re

client = openreview.Client(baseurl='https://api.openreview.net', username='amanda.stent@gmail.com', password='wed07oct')

with open("sitedata/papers.jsonold") as f:
    papers = json.load(f)
for paper in papers.values():
    print(paper["UID"])
    id = re.search(r'(\d+)', paper["UID"])[1]
    if int(id) > 40:
        for field in ["code", "data", "poster", "slides", "paper"]:
            if field in paper:
                id = re.search(r'id=([^&]+)', paper[field])[1]
                ext = re.search(r'name=([^&]+)', paper[field])
                if ext == None:
                    ext = 'pdf'
                else:
                    ext = ext[1]
                print(id, paper[field], ext)
                response = client.get_attachment(id, ext)
                if field in ["code", "data"]:
                    open("static/paperfiles/" + paper["UID"] + "_" + field + ".zip", "wb").write(response)
                    paper[field] = "static/paperfiles/" + paper["UID"] + "_" + field + ".zip"
                else:
                    open("static/paperfiles/" + paper["UID"] + "_" + field + ".pdf", "wb").write(response)
                    paper[field] = "static/paperfiles/" + paper["UID"] + "_" + field + ".pdf"
                
with open("papers.json", "w") as f:
    papers = json.dump(papers, f)
