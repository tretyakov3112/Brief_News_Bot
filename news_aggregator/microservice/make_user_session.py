# make_user_session.py
from telethon.sync import TelegramClient
from config import api_id, api_hash

with TelegramClient('gazp', api_id, api_hash) as client:
    print("User session ready")
