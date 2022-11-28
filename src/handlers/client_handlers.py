from pyrogram import Client, filters, types
from pyrogram import enums
from pyrogram.handlers import MessageHandler

from create_bot import db
from src.funcs.funcs import is_admin, delete_messages, generate_call_messages
from src.funcs.decors import error_catcher, rules_message
from src.consts import (START_MESSAGE, NOT_GROUP_ADMIN, CANNOT_CHANGE_PERMISSIONS, NOTIFY_PERMISSION_CHANGED, TURN_ON,
                        TURN_OFF, CALL_TITLE, CANNOT_CALL_ALL)


async def hello(_: Client, message: types.Message):
    await message.reply_text(START_MESSAGE)


# Change the "notify_for_all" permission, only for supergroup admins
@error_catcher
@rules_message(db)
async def call_perm(client: Client, message: types.Message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await delete_messages(await message.reply_text(f"{NOT_GROUP_ADMIN}, {CANNOT_CHANGE_PERMISSIONS}"),
                                     message)

    notify_flag = not db.get_notify_permission(message.chat.id)
    db.change_notify_permission(message.chat.id, notify_flag)
    await message.reply_text(NOTIFY_PERMISSION_CHANGED.format(TURN_ON if notify_flag else TURN_OFF),
                             reply_to_message_id=message.id)


# Do a lot of messages with notifies and author's message as title
@error_catcher
@rules_message(db)
async def notify_all(client: Client, message: types.Message):
    if not (await is_admin(client, message.chat.id, message.from_user.id) or db.get_notify_permission(message.chat.id)):
        return await delete_messages(message, await message.reply_text(f"{NOT_GROUP_ADMIN}, {CANNOT_CALL_ALL}",
                                                                       reply_to_message_id=message.id))

    message_title = "**" + ' '.join(message.text.split()[1:]) + "**"
    if message_title == '*' * 4:
        message_title += CALL_TITLE.format(message.from_user.username if message.from_user.username else message.from_user.first_name)
    message_title += "\n\n"

    async for bot_message in generate_call_messages(client.get_chat_members(message.chat.id)):
        await client.send_message(message.chat.id, f"{message_title}{bot_message}", parse_mode=enums.ParseMode.MARKDOWN)


def register_handlers_client(app: Client):
    app.add_handler(MessageHandler(hello, filters.command("start")))
    app.add_handler(MessageHandler(call_perm, filters.command("call_perm")))
    app.add_handler(MessageHandler(notify_all, filters.command("call")))
