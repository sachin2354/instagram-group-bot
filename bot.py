import os
import random
import time
from instagrapi import Client

# ✅ Fetch credentials from environment variables correctly
USERNAME = os.environ.get("s4bkabaap90")
PASSWORD = os.environ.get("Oggy420")

# Replace with your Instagram GROUP thread IDs for your test group
GROUP_THREAD_IDS = [
    "8928978693886302",  # replace with your test group's thread ID
]

MESSAGES = [
    "ujjwal kese bhagi r9di 😊",
    "rishabh bhen jail ka khana kesa laga 🤣!",
    "vishal bhabhi bhag mat cudakkd?",
    "preeti ki shut wet💧"
]

MIN_DELAY = 300    # 5 min
MAX_DELAY = 900    # 15 min

cl = Client()
try:
    cl.login(USERNAME, PASSWORD)
    print("✅ Logged in successfully.")
except Exception as e:
    print(f"❌ Login failed: {e}")
    exit()

def send_group_messages_forever():
    while True:
        for thread_id in GROUP_THREAD_IDS:
            try:
                message = random.choice(MESSAGES)
                cl.direct_send(message, [], thread_ids=[thread_id])
                print(f"✅ Sent to group {thread_id}: {message}")
            except Exception as e:
                print(f"❌ Failed to send to group {thread_id}: {e}")
            delay = random.randint(MIN_DELAY, MAX_DELAY)
            print(f"⏳ Sleeping {delay} seconds before next message.")
            time.sleep(delay)

if __name__ == "__main__":
    send_group_messages_forever()
