from instagrapi import Client
import random
import time
from datetime import datetime

USERNAME = "s4bkabaap90"
PASSWORD = "Oggy420"

# ---------- Load group IDs ----------
with open("group_ids.txt", "r") as f:
    group_ids = [line.strip() for line in f if line.strip()]

# ---------- Load messages ----------
with open("messages.txt", "r", encoding="utf-8") as f:
    messages = [line.strip() for line in f if line.strip()]

cl = Client()

try:
    cl.login(USERNAME, PASSWORD)
    print("✅ Logged in successfully.")
except Exception as e:
    print(f"❌ Login failed: {e}")
    exit()

def send_message_to_groups():
    message = random.choice(messages)
    for group_id in group_ids:
        try:
            cl.direct_send(message, [], thread_ids=[group_id])
            print(f"✅ Sent to {group_id}: {message}")
            time.sleep(random.uniform(10, 20))  # Delay between messages
        except Exception as e:
            print(f"❌ Failed to send to {group_id}: {e}")

while True:
    current_hour = datetime.now().hour
    if 1 <= current_hour < 6:
        print("😴 Resting from 1 AM to 6 AM. Sleeping for 1 hour...")
        time.sleep(3600)  # Sleep 1 hour during rest period
    else:
        send_message_to_groups()
        sleep_time = random.uniform(900, 1800)  # Sleep 15–30 min between rounds
        print(f"⏳ Sleeping for {sleep_time/60:.2f} minutes before next round...")
        time.sleep(sleep_time)
