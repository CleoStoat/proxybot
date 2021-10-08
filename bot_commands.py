from helpers.command_helpers import CommandData
from service_layer.commands_handlers.help import help_cmd

COMMANDS = [
    CommandData(
        callback=help_cmd,
        name="help",
        description="Display the help message",
        hidden=True,
    ),
]
