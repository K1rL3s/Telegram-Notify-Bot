import sqlite3
from enum import Enum
from typing import Literal


# Table names used as lists
class ListTables(Enum):
    BLACKLIST = 'blacklist'
    ADMINLIST = 'adminlist'


CHATS_PERMISSIONS_TABLE = """CREATE TABLE IF NOT EXISTS "chats_permissions" (
                               "chat_id" INTEGER NOT NULL UNIQUE,
                               "notify_for_all" INTEGER NOT NULL,
                               PRIMARY KEY("chat_id")
                             )"""
BLACKLIST_TABLE = f"""CREATE TABLE IF NOT EXISTS "{ListTables.BLACKLIST.value}" (
                       "user_id" INTEGER NOT NULL UNIQUE,
                       PRIMARY KEY("user_id")
                     )"""
ADMINLIST_TABLE = f"""CREATE TABLE IF NOT EXISTS "{ListTables.ADMINLIST.value}" (
                       "user_id" INTEGER NOT NULL UNIQUE,
                       PRIMARY KEY("user_id")
                     )"""
TABLES = (CHATS_PERMISSIONS_TABLE, BLACKLIST_TABLE, ADMINLIST_TABLE)

ADMINS = (929302216,)  # @K1rLes (author) | AKA. root ids, which cannot be removed from the database


class Database:
    def __init__(self, db_name: str = "notify_bot.sqlite"):
        self.db = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.db.cursor()
        for table in TABLES:
            self.cursor.execute(table)
            self.db.commit()
        for user_id in ADMINS:
            self.cursor.execute(f"INSERT OR REPLACE INTO {ListTables.ADMINLIST.value} VALUES (?)", (user_id,))
            self.db.commit()

    # TODO: Изменить запрос, если будет больше одного параметра в таблице (может некорректно работать)
    def change_notify_permission(self, chat_id: int, change: bool):
        self.cursor.execute("INSERT OR REPLACE INTO chats_permissions (chat_id, notify_for_all) VALUES (?, ?)",  # <-
                            (chat_id, int(change)))
        self.db.commit()

    def get_notify_permission(self, chat_id: int) -> bool:
        notify_perm = self.cursor.execute("SELECT notify_for_all FROM chats_permissions WHERE chat_id = ?",
                                          (chat_id,)).fetchone()
        return bool(notify_perm[0]) if notify_perm else False  # Stored as 0 or 1

    def add_to_list(self, author_id: int, user_id: int,
                    table: Literal[ListTables.BLACKLIST, ListTables.ADMINLIST]) -> bool:
        if not self.is_in_list(author_id, ListTables.ADMINLIST):
            return False
        if self.is_in_list(user_id, ListTables.ADMINLIST) or user_id in ADMINS:
            return False
        if author_id == user_id:
            return False
        self.cursor.execute(f"INSERT OR REPLACE INTO {table.value} (user_id) VALUES (?)", (user_id,))
        self.db.commit()
        return True

    def delete_from_list(self, author_id: int, user_id: int,
                         table: Literal[ListTables.BLACKLIST, ListTables.ADMINLIST]) -> bool:
        if not self.is_in_list(author_id, ListTables.ADMINLIST):
            return False
        if author_id == user_id:
            return False
        if user_id in ADMINS:
            return False
        self.cursor.execute(f"DELETE FROM {table.value} WHERE user_id = (?)", (user_id,))
        self.db.commit()
        return True

    def is_in_list(self, user_id: int, table: Literal[ListTables.BLACKLIST, ListTables.ADMINLIST]) -> bool:
        result = self.cursor.execute(f"SELECT * FROM {table.value} WHERE user_id = (?)", (user_id,)).fetchone()
        return result is not None
