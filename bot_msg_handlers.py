from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler

from service_layer.msg_handlers.new_message import new_message_msg_handler

MSG_HANDLERS = [
    MessageHandler(
        filters=Filters.update,
        callback=new_message_msg_handler,
    ),
]
