from pyrogram import Client

from src.database import Database
from config import bot_token, api_id, api_hash


app = Client(bot_token=bot_token, api_id=api_id, api_hash=api_hash, name="bot")
db = Database()
