import requests
import json
import re

KOMGA_URL = "http://192.168.123.45:25600"
KOMGA_USER = "admin@komga.com"
KOMGA_PASSWORD = "password"

KOMGA_SESSION = requests.Session()
KOMGA_SESSION.auth = (KOMGA_USER, KOMGA_PASSWORD)

ARTICLES = ["a", "an", "the", "A", "An", "The"]

series_list = []
page = 0
while True:
    series_response = KOMGA_SESSION.get(f"{KOMGA_URL}/api/v1/series?deleted=false&page={page}&size=20")

    if not series_response.ok:
        print(f"Error: {series_response.status_code}: {series_response.content}")
        exit(1)

    print(f"Processing series page {page} of {json.loads(series_response.content).get('totalPages')}")
    page += 1

    if json.loads(series_response.content).get("empty"):
        break

    komga_series_list = json.loads(series_response.content).get("content")
    for komga_series in komga_series_list:
        title = komga_series.get("metadata").get("title")
        article_match = re.match(rf"\b({'|'.join(ARTICLES)})\b", title)
        if article_match:
            series_list.append({"id": komga_series.get("id"), "title": title, "article_match": article_match})

print(f"Found {len(series_list)} series with article in title")

for series in series_list:
    new_title = series.get("title")[series.get("article_match").end():] + ", " + series.get("article_match").group()
    print(f"Renaming \"{series.get('title')}\" to \"{new_title}\"")
    renaming_response = KOMGA_SESSION.patch(f"{KOMGA_URL}/api/v1/series/{series.get('id')}/metadata",
                                            json={"titleSort": new_title, "titleSortLock": True})

    if not renaming_response.ok:
        print(f"Error: {renaming_response.status_code}: {renaming_response.content}")
        exit(1)
