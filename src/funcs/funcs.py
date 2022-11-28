import asyncio
import typing

import pyrogram
from pyrogram.errors import RPCError

from src.consts import DELETE_DELAY


# Check if the user is a group admin
async def is_admin(client: pyrogram.Client, chat_id: int, user_id: int) -> bool:
    try:
        async for user in client.get_chat_members(chat_id, filter=pyrogram.enums.ChatMembersFilter.ADMINISTRATORS):
            if user.user.id == user_id:
                return True
        return False
    except RPCError:
        return False


# Delete messages after a delay, used to remove invalid command calls
async def delete_messages(*messages: pyrogram.types.Message) -> None:
    await asyncio.sleep(DELETE_DELAY)
    for message in messages:
        try:
            await message.delete()
        except RPCError:
            pass


# Generate messages for "/call" command
async def generate_call_messages(users: typing.AsyncGenerator[pyrogram.types.ChatMember, None]) \
                                 -> typing.Optional[typing.AsyncGenerator[str, None]]:
    i = 1
    message = ''
    async for user in users:
        try:
            message += f"[{i}](tg://user?id={user.user.id}) "
        except (RPCError, AttributeError):
            message += f"{i} "
        if i == 7:
            yield message
            i = 0
            message = ''
        i += 1
    if message:
        yield message
