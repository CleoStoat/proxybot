from helpers.command_helpers import CommandData
from service_layer.commands_handlers.help import help_cmd
from service_layer.commands_handlers.send import send_cmd

COMMANDS = [
    CommandData(
        callback=help_cmd,
        name="help",
        description="Display the help message",
        hidden=True,
    ),
    CommandData(
        callback=send_cmd,
        name="s",
        description="Send a message to a chat",
        hidden=True,
    ),
]
