import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

import smtplib
from email.message import EmailMessage

load_dotenv()
KOMGA_URL = os.getenv("KOMGA_URL")
KOMGA_USER = os.getenv("KOMGA_USER")
KOMGA_PASSWORD = os.getenv("KOMGA_PASSWORD")

NOTIFICATION_INTERVAL = 2  # days
EMAIL_ADDRESS = "mail@mail.com"
EMAIL_PASSWORD = "password"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 25

s = requests.Session()

users = json.loads(
    s.get(f"{KOMGA_URL}/api/v2/users",
          auth=(KOMGA_USER, KOMGA_PASSWORD)).content
)

all_libraries = [l["id"] for l in json.loads(
    s.get(f"{KOMGA_URL}/api/v1/libraries").content
)]

emails = []
for KOMGA_USER in users:
    if KOMGA_USER["sharedAllLibraries"]:
        emails.append({"email": KOMGA_USER["email"], "libraries": all_libraries})
    else:
        emails.append({"email": KOMGA_USER["email"], "libraries": KOMGA_USER["sharedLibrariesIds"]})

books = []
page = 0
while True:
    books_response = json.loads(
        s.get(f"{KOMGA_URL}/api/v1/books?media_status=READY&page={page}&size=20&sort=createdDate,desc").content
    )["content"]
    page += 1
    for book in books_response:
        if (datetime.strptime(book["created"], "%Y-%m-%dT%H:%M:%S%z").timestamp()
                < (datetime.utcnow() - timedelta(days=NOTIFICATION_INTERVAL)).timestamp()):
            break
        books.append({"book": book["seriesTitle"] + " #" + book["metadata"]["number"].zfill(4)
                     + " - " + book["metadata"]["title"], "library": book["libraryId"]})
    else:
        continue
    break

for email in emails:
    mail_text = f"New books have been added to your libraries:\n"
    book_count = 0
    for b in books:
        if b["library"] in email["libraries"]:
            book_count += 1
            mail_text += f" - {b['book']}\n"
    email["mail_text"] = mail_text + f"Total: {book_count} books"

for email in emails:
    msg = EmailMessage()
    msg['Subject'] = "New books added to your libraries"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email["email"]
    msg.set_content(email["mail_text"])

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
