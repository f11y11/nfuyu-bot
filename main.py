import logging, os, asyncio
from dotenv import load_dotenv
from bot.bot import main

load_dotenv()

logging.basicConfig(level='INFO')

if __name__ == '__main__':
    if TOKEN := os.environ.get('TOKEN'):
        print('Starting bot')
        asyncio.run(main(TOKEN))
    else:
        print('(!) No TOKEN in .env')
        print('(?) Generate an example .env file using cp .env-template .env')
