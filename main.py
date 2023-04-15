import logging
import os
import asyncio

from dotenv import load_dotenv
from bot.bot import main, config

# Set up logging from config
if logging_data := config.get('logging'):
    if logging_level := logging_data.get('level'):
        if logging_level not in (
            'error',
            'info',
            'debug',
            'critical'
        ):
            logging_level = 'info'

    if logging_filename := logging_data.get('filename'):
        if not logging_filename.endswith('.log'):
            logging_filename = logging_filename + '.log'

    logging_console: bool = logging_data.get('console', False)

    logging.basicConfig(level=getattr(logging, logging_level.upper()), filename=logging_filename)
    if logging_console:
        logging.getLogger().addHandler(logging.StreamHandler())


load_dotenv()

if __name__ == '__main__':
    if TOKEN := os.environ.get('TOKEN'):
        logging.info('Starting bot')
        asyncio.run(main(TOKEN))
    else:
        logging.error('No TOKEN in .env')
        logging.error('Generate an example .env file using cp .env-template .env')
