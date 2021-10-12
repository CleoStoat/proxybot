from telegram import Update
from telegram.ext.callbackcontext import CallbackContext

from service_layer.unit_of_work import AbstractUnitOfWork
import config


def help_cmd(
    update: Update, context: CallbackContext, uow: AbstractUnitOfWork
) -> None:
    bot_chat: int = config.get_bot_group_id()
    if update.effective_chat.id != bot_chat:
        return

    text = f"Help for {context.bot.bot.username}\n\n"

    from bot_commands import COMMANDS    
    for cmd in COMMANDS:
        text += f"/{cmd.name} - {cmd.description}\n"

    update.effective_message.reply_text(text=text)