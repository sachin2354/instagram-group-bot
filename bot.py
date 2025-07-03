from instagrapi import Client
import random
import time
from datetime import datetime
import imaplib
import email
import re

# ---------- Configuration ----------
USERNAME = "s4bkabaap90"
PASSWORD = "Oggy420"
EMAIL_USER = "sachinrndi877@gmail.com"
EMAIL_PASS = "SERVEROFF"  # Use app password if using Gmail

# ---------- Load group IDs ----------
with open("group_ids.txt", "r") as f:
    group_ids = [line.strip() for line in f if line.strip()]

# ---------- Load messages ----------
with open("messages.txt", "r", encoding="utf-8") as f:
    messages = [line.strip() for line in f if line.strip()]

cl = Client()

# ---------- Auto-fetch IG Code ----------
def get_latest_instagram_code():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")

        result, data = mail.search(None, '(FROM "security@mail.instagram.com")')
        mail_ids = data[0]
        id_list = mail_ids.split()
        if not id_list:
            return None
        latest_email_id = id_list[-1]

        result, data = mail.fetch(latest_email_id, "(RFC822)")
        raw_email = data[0][1]
        raw_email_string = raw_email.decode("utf-8")
        message = email.message_from_string(raw_email_string)

        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    email_body = part.get_payload(decode=True).decode("utf-8")
        else:
            email_body = message.get_payload(decode=True).decode("utf-8")

        code_match = re.search(r'(\\d{6})', email_body)
        if code_match:
            code = code_match.group(1)
            print(f"🔐 Auto-fetched code: {code}")
            return code
        else:
            return None
    except Exception as e:
        print(f"❌ Error fetching code: {e}")
        return None

# ---------- Challenge Code Handler ----------
def challenge_code_handler(username, choice):
    print(f"🔄 Waiting for Instagram verification code to {choice}...")
    for attempt in range(15):  # ~2.5 minutes max
        code = get_latest_instagram_code()
        if code:
            return code
        time.sleep(10)
    print("❌ Could not fetch automatically, please enter manually:")
    return input("Enter the 6-digit code manually: ")

cl.challenge_code_handler = challenge_code_handler

# ---------- Login ----------
try:
    cl.login(USERNAME, PASSWORD)
    print("✅ Logged in successfully.")
except Exception as e:
    print(f"❌ Login failed: {e}")
    exit()

# ---------- Sending Messages ----------
def send_message_to_groups():
    message = random.choice(messages)
    for group_id in group_ids:
        try:
            cl.direct_send(message, [], thread_ids=[group_id])
            print(f"✅ Sent to {group_id}: {message}")
            time.sleep(random.uniform(10, 20))  # Delay between messages
        except Exception as e:
            print(f"❌ Failed to send to {group_id}: {e}")

# ---------- 24/7 Loop with 1 AM - 6 AM rest ----------
while True:
    current_hour = datetime.now().hour
    if 1 <= current_hour < 6:
        print("😴 Resting from 1 AM to 6 AM. Sleeping for 1 hour...")
        time.sleep(3600)
    else:
        send_message_to_groups()
        sleep_time = random.uniform(900, 1800)  # 15–30 min between rounds
        print(f"⏳ Sleeping for {sleep_time/60:.2f} minutes before next round...")
        time.sleep(sleep_time)
