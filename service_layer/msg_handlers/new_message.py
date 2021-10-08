from telegram import Update
from telegram.ext.callbackcontext import CallbackContext

from service_layer.unit_of_work import AbstractUnitOfWork
from service_layer.msg_handlers.copy_message import copy_message_msg_handler
from service_layer.msg_handlers.update_proxy_chat import update_proxy_chat_msg_handler



def new_message_msg_handler(
    update: Update, context: CallbackContext, uow: AbstractUnitOfWork
) -> None:
    update_proxy_chat_msg_handler(update, context, uow)
    copy_message_msg_handler(update, context, uow)