import logging
import os
import asyncio

from dotenv import load_dotenv
from bot.bot import main, config

logging_data = config.get("logging", {})
if not isinstance(logging_data, dict):
    logging_data = dict()


if not os.environ.get("TOKEN"):
    load_dotenv()

if level := logging_data.get("level"):
    handlers = []
    formatter = logging.Formatter("%(asctime)s %(name)-16s %(levelname)-8s %(message)s")
    if filename := logging_data.get("filename"):
        if not filename.endswith(".log"):
            filename += ".log"

        file_handler = logging.FileHandler(filename)
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)
    if logging_data.get("console"):
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        handlers.append(stream_handler)
    logging.basicConfig(level=getattr(logging, level.upper()), handlers=handlers)

if __name__ == "__main__":
    if TOKEN := os.environ.get("TOKEN"):
        logging.info("Starting bot")
        asyncio.run(main(TOKEN))
    else:
        logging.error("No TOKEN in .env")
        logging.error("Generate an example .env file using cp .env-template .env")
