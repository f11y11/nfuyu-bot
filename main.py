import logging, os
from dotenv import load_dotenv
from bot.bot import bot, config

load_dotenv()

logging.basicConfig(level='INFO')

if __name__ == '__main__':
    TOKEN = os.environ.get('TOKEN')
    print('Starting bot')
    bot.run(TOKEN)
