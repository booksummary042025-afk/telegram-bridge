import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from flask import Flask
from threading import Thread

# 1. Create a tiny fake website
app = Flask('')
@app.route('/')
def home():
    return "Bridge is alive!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# 2. Your Bridge Code
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
SOURCE_ID = int(os.environ.get("SOURCE_ID"))
TARGET_ID = int(os.environ.get("TARGET_ID"))

async def start_bridge():
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    await client.start()
    print("✅ Bridge is running!")

    @client.on(events.NewMessage(chats=SOURCE_ID))
    async def handler(event):
        if event.text:
            await client.send_message(TARGET_ID, event.text)
    
    await client.run_until_disconnected()

if __name__ == "__main__":
    # Start the fake website in a separate thread
    t = Thread(target=run_flask)
    t.start()
    # Start the Telegram bridge
    asyncio.run(start_bridge())
