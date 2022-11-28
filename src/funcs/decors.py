import sys
import traceback

import pyrogram
from pyrogram import enums

from src.funcs import delete_messages
from src.database import Database, ListTables
from src.consts import YOU_ARE_BLACKLISTED, NOT_BOT_ADMIN, NOT_A_SUPERGROUP


# Decorator that allows messages that match the conditions
def rules_message(db: Database):
    def decorator(func):
        async def tg_func(client: pyrogram.Client, message: pyrogram.types.Message):
            if db.is_in_list(message.from_user.id, ListTables.BLACKLIST):
                return await delete_messages(message, await client.send_message(message.chat.id, YOU_ARE_BLACKLISTED,
                                                                                reply_to_message_id=message.id))
            if message.chat.type != enums.ChatType.SUPERGROUP:
                return await delete_messages(message, await message.reply_text(
                                             NOT_A_SUPERGROUP.format(enums.ChatType.SUPERGROUP, message.chat.type),
                                             parse_mode=enums.ParseMode.MARKDOWN))
            await func(client, message)
        return tg_func
    return decorator


# Decorator that allows messages only from admins
def admin_command(db: Database):
    def decorator(func):
        async def tg_func(client: pyrogram.Client, message: pyrogram.types.Message):
            if not db.is_in_list(message.from_user.id, ListTables.ADMINLIST):
                return await delete_messages(message, await client.send_message(message.chat.id, NOT_BOT_ADMIN,
                                                                                reply_to_message_id=message.id))
            await func(client, message)
        return tg_func
    return decorator


# Decorator AKA. logging, but in terminal
def error_catcher(func):
    async def tg_func(*args, **kwargs):
        try:
            await func(*args, **kwargs)
        except Exception:
            print(f"{func.__name__}: {sys.exc_info()} {traceback.extract_tb(sys.exc_info()[2])}")
    return tg_func
