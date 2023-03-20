import requests
import json

import os
from dotenv import load_dotenv

load_dotenv()
komga_url = os.getenv("KOMGA_URL")
user = os.getenv("KOMGA_USER")
password = os.getenv("KOMGA_PASSWORD")
s = requests.Session()

pages = json.loads(
    s.get(f"{komga_url}/api/v1/series?search=The&deleted=false&page=0&size=10",
          auth=(user, password)).content
        )["totalPages"]

for i in range(pages):
    series_list = json.loads(
                    s.get(f"{komga_url}/api/v1/series?search=The&deleted=false&page={i}&size=10").content
                  )["content"]
    for series in series_list:
        title = series["metadata"]["title"]
        if title.startswith(("the ", "a ", "an ","The ", "A ", "An")):
            title_split = title.split()
            s.patch(f"{komga_url}/api/v1/series/{series['id']}/metadata",
                    json={"titleSort": " ".join(title_split[1:]) + ", " + title_split[0], "titleSortLock": True})
