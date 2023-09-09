import logging
import os
import asyncio

from dotenv import load_dotenv
from bot.bot import main, config

logging_data = config.get("logging")
load_dotenv()

if __name__ == "__main__":
    if logging_level := logging_data.get("level"):
        if logging_level and logging_level not in (
            "error",
            "info",
            "debug",
            "critical",
        ):
            logging_level = "info"

    if logging_filename := logging_data.get("filename"):
        if not logging_filename.endswith(".log"):
            logging_filename = logging_filename + ".log"

    if logging_data.get("console", False):
        logging.getLogger().addHandler(logging.StreamHandler())
    elif not logging_filename:
        print(
            """
            You have enabled logging but set both console and filename blank.
            Nothing will be printed to the console or written to a file. 
            """
        )

    logging.basicConfig(
        level=getattr(logging, logging_level.upper()), filename=logging_filename
    )

    if TOKEN := os.environ.get("TOKEN"):
        logging.info("Starting bot")
        asyncio.run(main(TOKEN))
    else:
        logging.error("No TOKEN in .!env")
        logging.error("Generate an example .env file using cp .env-template .env")
