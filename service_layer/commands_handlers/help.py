from telegram import Update
from telegram.ext.callbackcontext import CallbackContext

from service_layer.unit_of_work import AbstractUnitOfWork
import config


def help_cmd(
    update: Update, context: CallbackContext, uow: AbstractUnitOfWork
) -> None:
    text = f"Help for {context.bot.bot.username}\n"
    text += "/help - display this message"
    update.effective_message.reply_text(text=text)