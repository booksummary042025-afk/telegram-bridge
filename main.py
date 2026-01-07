import os, asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home(): return "Bridge is alive!"

def run_flask(): app.run(host='0.0.0.0', port=10000)

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
SOURCE_ID = int(os.environ.get("SOURCE_ID"))
TARGET_ID = int(os.environ.get("TARGET_ID"))

async def start_bridge():
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    await client.start()
    print("✅ BRIDGE CONNECTED SUCCESSFULLY")

    @client.on(events.NewMessage) # Listen to EVERYTHING first to debug
    async def handler(event):
        # This will print every message you see in the Render Logs
        # print(f"DEBUG: Message from {event.chat_id}: {event.text}")
        
        if event.chat_id == SOURCE_ID:
            await client.send_message(TARGET_ID, event.text)
            print("🚀 FORWARD SUCCESSFUL")

    await client.run_until_disconnected()

if __name__ == "__main__":
    Thread(target=run_flask).start()
    asyncio.run(start_bridge())
