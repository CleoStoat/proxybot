from telegram import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.messageid import MessageId

from service_layer.unit_of_work import AbstractUnitOfWork
import config


def update_proxy_chat_msg_handler(
    update: Update, context: CallbackContext, uow: AbstractUnitOfWork
) -> None:
    owner_chat: int = config.get_bot_owner_user_id()

    # if update.effective_chat.id == owner_chat:
    #     return

    chat_id: int = update.effective_chat.id
    name: str = ""

    if update.effective_chat.type == update.effective_chat.PRIVATE:
        name = update.effective_chat.full_name
        name+= " "
        username = update.effective_chat.username
        name += f"@{username}" if username is not None else ""
    else:
        name = update.effective_chat.title

    with uow:
        proxy_chat = uow.repo.find_proxychat(chat_id)

        if proxy_chat is None:
            uow.repo.add_proxychat(chat_id, name)
            text = f"New chat added:\n\nName: {name}\nid: {chat_id}"
            context.bot.send_message(chat_id=owner_chat, text=text)
            uow.commit()
            return
        
        if proxy_chat.name != name:
            uow.repo.set_proxychat_name(chat_id, name)
            text = f"Updated chat name:\n\nOld name: {proxy_chat.name}\nNew name: {name}\nid: {chat_id}"
            context.bot.send_message(chat_id=owner_chat, text=text)
            uow.commit()
            return

        uow.commit()
