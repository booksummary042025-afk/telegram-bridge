import os
import asyncio
import logging
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Setup logging to see what's happening in Koyeb logs
logging.basicConfig(level=logging.INFO)

# Get variables from Koyeb settings
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
SOURCE_ID = int(os.environ.get("SOURCE_ID"))
TARGET_ID = int(os.environ.get("TARGET_ID"))

async def main():
    # Use StringSession so it doesn't need a local file or phone code
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    
    await client.start()
    logging.info("✅ Bridge is ACTIVE on Koyeb!")

    @client.on(events.NewMessage(chats=SOURCE_ID))
    async def handler(event):
        if event.text:
            # Re-posts the message so your Bot can see it
            await client.send_message(TARGET_ID, event.text)
            logging.info(f"Forwarded message from {SOURCE_ID}")

    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
