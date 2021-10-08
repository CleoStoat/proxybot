from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    Boolean,
    String
)
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import mapper

from domain.model import CopiedMessage, ProxyChat
import config

metadata = MetaData()

copied_messages = Table(
    "copied_messages",
    metadata,
    Column("origin_chat_id", Integer, primary_key=True, autoincrement=False),
    Column("origin_message_id", Integer, primary_key=True, autoincrement=False),
    Column("copied_message_id", Integer, primary_key=True, autoincrement=False),
)

proxy_chats = Table(
    "proxy_chats",
    metadata,
    Column("chat_id", Integer, primary_key=True, autoincrement=False),
    Column("name", String(255)),
    Column("listening", Boolean, default=True),
)

def start_mappers():
    mapper(CopiedMessage, copied_messages)
    mapper(ProxyChat, proxy_chats)


def create_tables():
    engine = create_engine(config.get_sqlite_uri())
    metadata.create_all(engine)
