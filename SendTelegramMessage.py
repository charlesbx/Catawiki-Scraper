from sys import argv
import asyncio
from telegram import Bot
from config import *

async def send_telegram_message(message):
    bot = Bot(token=TelegramToken)
    for chat_id in TelegramChatID:
        await bot.send_message(chat_id=chat_id, text=message)
        print(f"Message sent to {chat_id}")
        
if __name__ == "__main__":
    if len(argv) < 2:
        print("Usage: python SendTelegramMessage.py <message>")
        exit(1)
    message = argv[1].replace("'", "")
    asyncio.run(send_telegram_message(message))