import time
import random
import os
import requests

def load_messages():
    with open("messages.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def log(message):
    with open("log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")
    print(message)

def get_inbox(session, headers):
    response = session.get("https://i.instagram.com/api/v1/direct_v2/inbox/", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        log(f"Failed to fetch inbox: {response.status_code}")
        return None

def is_group_thread(thread):
    return len(thread.get("users", [])) > 1

def send_message(session, headers, thread_id, text):
    url = f"https://i.instagram.com/api/v1/direct_v2/threads/{thread_id}/items/"
    data = {"text": text, "action": "send_item"}
    response = session.post(url, headers=headers, data=data)
    return response.status_code == 200

def main():
    config = {
        "sessionid": os.getenv("SESSION_ID"),
        "user_agent": os.getenv("USER_AGENT", "Instagram 155.0.0.37.107 Android"),
        "min_delay": float(os.getenv("MIN_DELAY", 0.2)),
        "max_delay": float(os.getenv("MAX_DELAY", 2.0))
    }

    messages = load_messages()
    session = requests.Session()
    session.cookies.set("sessionid", config["sessionid"])
    headers = {
        "User-Agent": config["user_agent"],
        "Content-Type": "application/x-www-form-urlencoded"
    }

    replied_threads = set()
    log("Bot started...")

    while True:
        inbox = get_inbox(session, headers)
        if inbox:
            threads = inbox.get("inbox", {}).get("threads", [])
            for thread in threads:
                thread_id = thread.get("thread_id")
                if not thread_id or thread_id in replied_threads:
                    continue
                if is_group_thread(thread):
                    msg = random.choice(messages)
                    delay = random.uniform(config["min_delay"], config["max_delay"])
                    time.sleep(delay)
                    if send_message(session, headers, thread_id, msg):
                        log(f"Replied to group {thread_id} with: {msg}")
                        replied_threads.add(thread_id)
        time.sleep(10)

if __name__ == "__main__":
    main()
