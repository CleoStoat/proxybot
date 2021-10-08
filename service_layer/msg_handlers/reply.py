from typing import Optional
from telegram import Update
from telegram.ext.callbackcontext import CallbackContext
from domain.model import ProxyChat

from service_layer.unit_of_work import AbstractUnitOfWork
import config


def reply_msg_handler(
    update: Update, context: CallbackContext, uow: AbstractUnitOfWork
) -> None:
    owner_chat: int = config.get_bot_owner_user_id()
    if update.effective_chat.id != owner_chat:
        return
    
    if update.effective_message.reply_to_message is None:
        return

    copied_message_id: int = update.effective_message.reply_to_message.message_id

    with uow:
        copied_message = uow.repo.find_copied_message(copied_message_id)

    if copied_message is None:
        return
    
    target_chat_id = copied_message.origin_chat_id
    target_message_id = copied_message.origin_message_id
    message_to_copy_id = update.effective_message.message_id

    try:
        context.bot.copy_message(
            chat_id=target_chat_id,
            from_chat_id=owner_chat,
            message_id=message_to_copy_id,
            reply_to_message_id=target_message_id,
        )
    except Exception:
        text = "Couldn't send message."
        update.effective_message.reply_text(text=text, quote=True)
        return

    text = "Message successfully delivered."
    update.effective_message.reply_text(text=text, quote=True)