from telegram import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.messageid import MessageId
from telegram.utils.helpers import escape_markdown as em

from service_layer.unit_of_work import AbstractUnitOfWork
import config


def copy_message_msg_handler(
    update: Update, context: CallbackContext, uow: AbstractUnitOfWork
) -> None:
    owner_chat: int = config.get_bot_owner_user_id()
    if update.effective_chat.id == owner_chat:
        return

    origin_chat_id: int = update.effective_chat.id
    with uow:
        proxy_chat = uow.repo.find_proxychat(origin_chat_id)

        if proxy_chat is not None:
            if proxy_chat.listening == False:
                return
        uow.commit()
    
    from_user_name: str
    from_chat_name: str

    from_user_name = update.effective_user.full_name
    from_user_name += " "
    username = update.effective_user.username
    from_user_name += f"@{username}" if username is not None else ""

    if update.effective_chat.type == update.effective_chat.PRIVATE:
        from_chat_name = from_user_name
    else:
        from_chat_name = update.effective_chat.title

    copied: MessageId

    try:
        copied: MessageId = update.effective_message.copy(owner_chat)
    except Exception:
        return

    origin_message_id: int = update.effective_message.message_id
    copied_message_id: int = copied.message_id

    with uow:
        uow.repo.add_copied_message(
            origin_chat_id, origin_message_id, copied_message_id
        )
        uow.commit()

    from_user_id: int = update.effective_user.id

    text = f"User name: {em(from_user_name, version=2)}\nChat name: {em(from_chat_name, version=2)}\nChat id: `{em(str(origin_chat_id), version=2)}`\nUser id: `{em(str(from_user_id), version=2)}`"
    copied2 = context.bot.send_message(
        chat_id=owner_chat, text=text, reply_to_message_id=copied_message_id, parse_mode="MarkdownV2"
    )
    
    with uow:
        uow.repo.add_copied_message(
            origin_chat_id, origin_message_id, copied2.message_id
        )
        uow.commit()
