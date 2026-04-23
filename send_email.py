import smtplib
import requests
import os
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dateutil import parser

nu = datetime.now().date()

# 📁 fil som sparar skickade events
FIL = "sent_events.txt"

try:
    with open(FIL, "r") as f:
        skickade = set(f.read().splitlines())
except:
    skickade = set()

polisapi = requests.get("https://polisen.se/api/events")
polisdata = polisapi.json()

nya_events = []
nya_ids = []

for data in polisdata:

    event_tid = parser.parse(data["datetime"]).date()
    plats = data["location"]["name"]
    text = (data["name"] + " " + data.get("summary", "")).lower()

    # dagens datum
    if event_tid != nu:
        continue

    # stockholm
    if "stockholm" not in plats.lower():
        continue

    # ta bort skräp
    if any(x in text for x in ["övning", "information", "samverkan"]):
        continue

    # riktiga brott
    if not any(x in text for x in [
        "misshandel", "stöld", "rån", "inbrott",
        "narkotika", "våld", "brand", "bedrägeri"
    ]):
        continue

    event_id = data["datetime"] + data["name"]

    # ❌ redan skickad
    if event_id in skickade:
        continue

    # ✔ ny event
    event_text = (
        f"{data['name']}\n"
        f"{data.get('summary', '').strip()}\n\n"
    )

    nya_events.append(event_text)
    nya_ids.append(event_id)

# inget nytt
if not nya_events:
    print("Inga nya brott")
    exit()

# mail text
email_text = "NYA BROTT STOCKHOLM\n\n"

for e in nya_events:
    email_text += e

# email
email_sender = "blake.joeseph08@gmail.com"
email_password = "rtmanuhhdoegvixq"
email_receiver = "blake.joeseph08@gmail.com"

message = MIMEMultipart()
message["From"] = email_sender
message["To"] = email_receiver
message["Subject"] = "Nya brott"

message.attach(MIMEText(email_text, "plain"))

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(email_sender, email_password)
server.sendmail(email_sender, email_receiver, message.as_string())
server.quit()

# 💾 spara nya events
with open(FIL, "a") as f:
    for eid in nya_ids:
        f.write(eid + "\n")

print("Nya brott skickade!")
