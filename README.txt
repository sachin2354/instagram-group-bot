📘 Instagram Group Auto-Reply Bot (Python)
---------------------------------------------------

🚀 FEATURES:
- Replies to all Instagram group chats instantly (0.2s to 2s delay)
- Uses your session ID to authenticate (no password needed)
- Random messages from messages.txt
- Safe delay to avoid bans
- Runs 24/7 on Replit or Railway

🛠 SETUP STEPS:

1. Open config.json and replace:
   "sessionid": "15649931872%3A8UwsLrkqBaOqz3%3A10%3AAYeKERHyah8DTYDEDZwfWtTkNczEPa6X5Iq8quDdew"
   with your actual Instagram sessionid from browser cookies.

2. Edit messages.txt to add your custom replies (one per line).

3. Run bot using:
   python insta_autoreply_bot.py

✅ Done! Bot will check group DMs every 10 seconds and reply once per group.

📌 TIP:
To run this on free server (Replit or Railway), copy all files there.
Make sure to keep your sessionid private.

