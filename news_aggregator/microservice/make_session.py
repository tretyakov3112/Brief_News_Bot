# make_bot_session.py
from telethon.sync import TelegramClient
from config import api_id, api_hash, bot_token

with TelegramClient('bot', api_id, api_hash) as bot:
    bot.start(bot_token=bot_token)
    print("bot.session создана")
