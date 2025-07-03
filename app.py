from instagrapi import Client
import random
import time
from datetime import datetime
import imaplib
import email
import re
import os
import json

# ---------- Configuration ----------
USERNAME = os.environ.get("s4bkabaap90")
PASSWORD = os.environ.get("Oggy420")
EMAIL_USER = os.environ.get("sachinrndi877@gmail.com")
EMAIL_PASS = os.environ.get("SERVEROFF")

# Load group IDs
with open("group_ids.txt", "r") as f:
    group_ids = [line.strip() for line in f if line.strip()]

# Load messages
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
        id_list = data[0].split()
        if not id_list:
            return None
        latest_email_id = id_list[-1]
        result, data = mail.fetch(latest_email_id, "(RFC822)")
        raw_email = data[0][1]
        message = email.message_from_bytes(raw_email)
        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    email_body = part.get_payload(decode=True).decode()
        else:
            email_body = message.get_payload(decode=True).decode()
        code_match = re.search(r'(\\d{6})', email_body)
        if code_match:
            return code_match.group(1)
        return None
    except Exception as e:
        print(f"IMAP error: {e}")
        return None

# ---------- Challenge Code Handler ----------
def challenge_code_handler(username, choice):
    print(f"Waiting for verification code to {choice}...")
    for _ in range(15):
        code = get_latest_instagram_code()
        if code:
            print(f"Fetched code: {code}")
            return code
        time.sleep(10)
    code_env = os.environ.get("IG_CODE")
    if code_env:
        print(f"Using IG_CODE from environment: {code_env}")
        return code_env
    print("Code could not be fetched automatically.")
    exit()

cl.challenge_code_handler = challenge_code_handler

# ---------- Persistent Login ----------
if os.path.exists("session.json"):
    with open("session.json", "r") as f:
        cl.set_settings(json.load(f))

try:
    cl.login(USERNAME, PASSWORD)
    with open("session.json", "w") as f:
        json.dump(cl.get_settings(), f)
    print("Logged in successfully.")
except Exception as e:
    print(f"Login failed: {e}")
    exit()

# ---------- Messaging Loop ----------
def send_message_to_groups():
    message = random.choice(messages)
    for group_id in group_ids:
        try:
            cl.direct_send(message, [], thread_ids=[group_id])
            print(f"Sent to {group_id}: {message}")
            time.sleep(random.uniform(10, 20))
        except Exception as e:
            print(f"Error sending to {group_id}: {e}")

while True:
    hour = datetime.now().hour
    if 1 <= hour < 6:
        print("Sleeping 1 hour (1 AM - 6 AM quiet hours)...")
        time.sleep(3600)
    else:
        send_message_to_groups()
        sleep_time = random.uniform(900, 1800)
        print(f"Sleeping {sleep_time/60:.2f} minutes before next round...")
        time.sleep(sleep_time)
