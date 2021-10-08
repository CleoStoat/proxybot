from telegram import Update
from telegram.ext.callbackcontext import CallbackContext

from service_layer.unit_of_work import AbstractUnitOfWork
import config


def send_cmd(
    update: Update, context: CallbackContext, uow: AbstractUnitOfWork
) -> None:
    owner_chat: int = config.get_bot_owner_user_id()
    if update.effective_chat.id != owner_chat:
        return
    
    if update.effective_message.reply_to_message is None:
        text = "No message specified."
        update.effective_message.reply_text(text=text, quote=True)
        return

    if len(context.args) < 1:
        text = "Tell me the chat id."
        update.effective_message.reply_text(text=text, quote=True)
        return

    chat_id: int 
    try:
        chat_id = int(context.args[0])
    except ValueError:
        text = "Invalid chat id."
        update.effective_message.reply_text(text=text, quote=True)
        return

    try:
        context.bot.copy_message(
            chat_id=chat_id,
            from_chat_id=owner_chat,
            message_id=update.effective_message.reply_to_message.message_id,
            )
    except Exception:
        text = "Couldn't send message."
        update.effective_message.reply_text(text=text, quote=True)
        return

    text = "Message successfully delivered."
    update.effective_message.reply_text(text=text, quote=True)