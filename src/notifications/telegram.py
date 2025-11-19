"""
Telegram notification client for sending auction alerts.
"""
from sys import argv
import asyncio
from typing import List
from telegram import Bot

from src.config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_IDS

async def send_telegram_message(message: str, chat_ids: List[str] = None) -> None:
    """
    Send a message to one or more Telegram chats.
    
    Args:
        message: The message text to send
        chat_ids: Optional list of chat IDs. If None, uses configured default.
    """
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    recipients = chat_ids or TELEGRAM_CHAT_IDS
    
    for chat_id in recipients:
        try:
            await bot.send_message(chat_id=chat_id, text=message)
            print(f"Message sent to {chat_id}")
        except Exception as e:
            print(f"Failed to send message to {chat_id}: {e}")
        
if __name__ == "__main__":
    if len(argv) < 2:
        print("Usage: python SendTelegramMessage.py <message>")
        exit(1)
    message = argv[1].replace("'", "")
    asyncio.run(send_telegram_message(message))