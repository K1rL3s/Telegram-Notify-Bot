from pyrogram import Client, filters, types
from pyrogram.handlers import MessageHandler

from create_bot import db
from src.database import ListTables
from src.funcs.decors import error_catcher, admin_command
from src.consts import ERROR_OCCURRED, ADDED_TO_LIST, DELETED_FROM_LIST


# Add user_id to db in table "adminlist" or "blacklist"
@error_catcher
@admin_command(db)
async def add_admin_bl(client: Client, message: types.Message):
    list_table = ListTables.ADMINLIST if message.command[0] == "add_admin" else ListTables.BLACKLIST
    user = await client.get_chat_member(message.chat.id, message.command[1])
    if not db.add_to_list(message.from_user.id, user.user.id, list_table):
        return await message.reply_text(ERROR_OCCURRED)
    await message.reply_text(ADDED_TO_LIST.format(user.user.username, list_table.value))


# Delete user_id from db from table "adminlist" or "blacklist"
@error_catcher
@admin_command(db)
async def del_admin_bl(client: Client, message: types.Message):
    list_table = ListTables.ADMINLIST if message.command[0] == "del_admin" else ListTables.BLACKLIST
    user = await client.get_chat_member(message.chat.id, message.command[1])
    if not db.delete_from_list(message.from_user.id, user.user.id, list_table):
        return await message.reply_text(ERROR_OCCURRED)
    await message.reply_text(DELETED_FROM_LIST.format(user.user.username, list_table.value))


def register_handlers_admin(app: Client):
    app.add_handler(MessageHandler(add_admin_bl, filters.command(["add_admin", "add_bl"])))
    app.add_handler(MessageHandler(del_admin_bl, filters.command(["del_admin", "del_bl"])))
