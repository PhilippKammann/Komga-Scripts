import requests
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()
KOMGA_URL = os.getenv("KOMGA_URL")
KOMGA_USER = os.getenv("KOMGA_USER")
KOMGA_PASSWORD = os.getenv("KOMGA_PASSWORD")

s = requests.Session()
ARTICLES = ["a", "an", "the", "A", "An", "The"]

pages = json.loads(
    s.get(f"{KOMGA_URL}/api/v1/series?&deleted=false&page=0&size=10",
          auth=(KOMGA_USER, KOMGA_PASSWORD)).content
        )["totalPages"]

for i in range(pages):
    series_list = json.loads(
                    s.get(f"{KOMGA_URL}/api/v1/series?search=The&deleted=false&page={i}&size=10").content
                  )["content"]
    for series in series_list:
        title = series["metadata"]["title"]
        m = re.match(f"\b({'|'.join(ARTICLES)})\b", title)
        if m:
            s.patch(f"{KOMGA_URL}/api/v1/series/{series['id']}/metadata",
                    json={"titleSort": title.replace(m.group(1), "").strip() + ", " + m.group(1),
                          "titleSortLock": True})
