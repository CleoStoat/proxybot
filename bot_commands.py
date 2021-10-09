from helpers.command_helpers import CommandData
from service_layer.commands_handlers.help import help_cmd
from service_layer.commands_handlers.send import send_cmd
from service_layer.commands_handlers.start_listening import start_listening_cmd
from service_layer.commands_handlers.stop_listening import stop_listening_cmd
from service_layer.commands_handlers.list_chats import list_chats_cmd

COMMANDS = [
    CommandData(
        callback=help_cmd,
        name="_help",
        description="Display the help message",
        hidden=True,
    ),
    CommandData(
        callback=start_listening_cmd,
        name="start_listening",
        description="start listening to a chat",
        hidden=True,
    ),
    CommandData(
        callback=stop_listening_cmd,
        name="stop_listening",
        description="stop listening to a chat",
        hidden=True,
    ),
    CommandData(
        callback=send_cmd,
        name="_s",
        description="Send a message to a chat",
        hidden=True,
    ),
    CommandData(
        callback=list_chats_cmd,
        name="_list",
        description="List known chats",
        hidden=True,
    ),
]
