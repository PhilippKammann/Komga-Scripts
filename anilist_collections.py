import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

KOMGA_URL = os.getenv("KOMGA_URL")
KOMGA_USER = os.getenv("KOMGA_USER")
KOMGA_PASSWORD = os.getenv("KOMGA_PASSWORD")
ANILIST_USERS = []  # ["user1", "user2"]
MANGA_LIBRARY = ""  # "YOUR LIBRARY ID HERE"
NOVEL_LIBRARY = ""  # "YOUR LIBRARY ID HERE"

s = requests.session()


def get_anilist_mangas(user):
    url = "https://graphql.anilist.co"
    query = '''
    query ($userName: String) {
        MediaListCollection(userName: $userName, type: MANGA) {
            lists {
                name
                entries {
                    media {
                        title {
                            english
                        }
                        format
                    }
                }
            }
        }
    }
    '''

    variables = {
        'userName': user
    }

    response = requests.post(url, json={'query': query, 'variables': variables})

    if response.status_code != 200:
        print(f'An error occurred: {response.content}')
        return
    data = json.loads(response.content)['data']['MediaListCollection']['lists']
    user_titles = [
        {"title": entry['media']["title"]["english"],
         "format": entry['media']["format"],
         "status": media_list["name"]}
        for media_list in data
        for entry in media_list['entries']
        if entry['media']['title']['english']
    ]
    return user_titles


def get_komga_titles(library_id):
    titles = json.loads(
        s.get(
            f"{KOMGA_URL}/api/v1/series?library_id={library_id}&unpaged=true",
            auth=(KOMGA_USER, KOMGA_PASSWORD),
        ).content
    )["content"]
    titles_dict = {title["metadata"]["title"]: title["id"] for title in titles}
    return titles_dict


def get_collection_by_name(collection_name):
    r = s.get(f"{KOMGA_URL}/api/v1/collections?search={collection_name}")
    if r.status_code != 200:
        return None

    data = json.loads(r.content)["content"]
    if not data:
        return None

    if data[0]["name"] == collection_name:
        return data[0]


def update_collection(collection, data):
    r = s.patch(f"{KOMGA_URL}/api/v1/collections/{collection['id']}", json=data)

    if r.status_code != 204:
        print(f"failed to update collection \"{collection['name']}\"")
        return

    print(f"updated collection \"{collection['name']}\"")


def create_collection(ids, user, anilist_type):
    if not ids:
        return
    ids = list(filter(None, ids))
    data = {
        "name": f"{user}'s {anilist_type} List",
        "ordered": False,
        "seriesIds": ids,
    }
    r = s.post(f"{KOMGA_URL}/api/v1/collections", json=data)
    if r.status_code != 200:
        old_collection = get_collection_by_name(f"{user}'s {anilist_type} List")
        if old_collection:
            update_collection(old_collection, data)
        else:
            print("failed to find existing collection")
    else:
        print(f"created collection \"{user}'s {anilist_type} List\" for user")


if __name__ == "__main__":
    if not KOMGA_URL:
        print("komgaUrl is missing\nEdit the variables at the top of the script.")
        exit()
    if not KOMGA_USER:
        print("user is missing\nEdit the variables at the top of the script.")
        exit()
    if not KOMGA_PASSWORD:
        print("password is missing\nEdit the variables at the top of the script.")
        exit()
    if not ANILIST_USERS:
        print("no anilist users specified\nEdit the variables at the top of the script.")
        exit()
    if not (MANGA_LIBRARY or NOVEL_LIBRARY):
        print("no library specified\nEdit the variables at the top of the script.")
        exit()

    for anilist_user in ANILIST_USERS:
        print(f"getting manga list for {anilist_user}")
        mangas = get_anilist_mangas(anilist_user)
        if not mangas:
            print("no eligible manga list found, skipping")
            continue

        if MANGA_LIBRARY:
            manga_titles = get_komga_titles(MANGA_LIBRARY)
            create_collection([manga_titles.get(fav["title"], None) for fav in mangas
                               if fav["format"] in ["MANGA", "ONE_SHOT"] and fav["status"] == "Reading"], anilist_user,
                              "Manga Reading")
            create_collection([manga_titles.get(fav["title"], None) for fav in mangas
                               if fav["format"] in ["MANGA", "ONE_SHOT"] and fav["status"] == "Planning"], anilist_user,
                              "Manga Planned")
            create_collection([manga_titles.get(fav["title"], None) for fav in mangas
                               if fav["format"] in ["MANGA", "ONE_SHOT"] and fav["status"]
                               in ["Completed Manga", "Completed Novel", "Completed One Shot"]], anilist_user,
                              "Manga Completed")
            # create_collection([manga_titles.get(fav["title"], None) for fav in mangas
            #                   if fav["format"] in ["MANGA", "ONE_SHOT"] and fav["status"] == "Dropped"], anilist_user,
            #                   "Manga Dropped")

        if NOVEL_LIBRARY:
            novel_titles = get_komga_titles(NOVEL_LIBRARY)
            create_collection([novel_titles.get(fav["title"], None) for fav in mangas
                               if fav["format"] in ["NOVEL"] and fav["status"] == "Reading"], anilist_user,
                              "Novel Reading")
            create_collection([novel_titles.get(fav["title"], None) for fav in mangas
                               if fav["format"] in ["NOVEL"] and fav["status"] == "Planning"], anilist_user,
                              "Novel Planned")
            create_collection([novel_titles.get(fav["title"], None) for fav in mangas
                               if fav["format"] in ["NOVEL"] and fav["status"]
                               in ["Completed Manga", "Completed Novel", "Completed One Shot"]], anilist_user,
                              "Novel Completed")
            # create_collection([novel_titles.get(fav["title"], None) for fav in mangas
            #                   if fav["format"] in ["NOVEL"] and fav["status"] == "Dropped"], anilist_user,
            #                   "Novel Dropped")
