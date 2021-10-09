from typing import List
from telegram import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.utils.helpers import escape_markdown as em

from service_layer.unit_of_work import AbstractUnitOfWork
import config
from domain.model import ProxyChat


def list_chats_cmd(
    update: Update, context: CallbackContext, uow: AbstractUnitOfWork
) -> None:
    owner_chat: int = config.get_bot_owner_user_id()
    if update.effective_chat.id != owner_chat:
        return

    proxy_chats: List[ProxyChat]

    with uow:
        proxy_chats = uow.repo.list_all_proxychats()
        uow.commit()


    text = "*Chats:*\n\n"
    for proxy_chat in proxy_chats:
        text += f"name: {em(str(proxy_chat.name), version=2)}\n"
        text += f"id: `{em(str(proxy_chat.chat_id), version=2)}`\n"
        text += f"listening: {em(str(proxy_chat.listening), version=2)}\n"
        text += "\n"

    update.effective_message.reply_text(text=text, quote=True, parse_mode="MarkdownV2")