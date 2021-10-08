import logging

from telegram.ext import Updater

import config
from adapters.orm import create_tables, start_mappers
from bot_commands import COMMANDS
from bot_msg_handlers import MSG_HANDLERS
from helpers.command_helpers import setup_bot
from service_layer.unit_of_work import SqlAlchemyUnitOfWork


def main():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    start_mappers()
    create_tables()

    updater = Updater(token=config.get_bot_token())

    # Instantiate SqlAlchemy Unit of Work
    uow = SqlAlchemyUnitOfWork()

    setup_bot(COMMANDS, MSG_HANDLERS, updater, uow)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
