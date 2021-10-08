from telegram import Update
from telegram.ext.callbackcontext import CallbackContext

from service_layer.unit_of_work import AbstractUnitOfWork
import config


def stop_listening_cmd(
    update: Update, context: CallbackContext, uow: AbstractUnitOfWork
) -> None:
    owner_chat: int = config.get_bot_owner_user_id()
    if update.effective_chat.id != owner_chat:
        return
    
    if len(context.args) < 1:
        text = "Specify chat id."
        update.effective_message.reply_text(text=text, quote=True)
        return

    chat_id: int

    try:
        chat_id = int(context.args[0])
    except ValueError:
        text = "Invalid chat id."
        update.effective_message.reply_text(text=text, quote=True)
        return

    with uow:
        uow.repo.set_proxychat_listening(chat_id=chat_id, listening=False)

    text = "Stopped listening."
    update.effective_message.reply_text(text=text, quote=True)