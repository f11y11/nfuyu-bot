import yaml
import logging

from discord.mentions import AllowedMentions
from discord.ext import commands
from discord.flags import Intents
from discord import Game
from string import Template


intents = Intents.all()
intents.presences = False

with open("config.yml", "r") as f:
    config: dict = yaml.safe_load(f)

am = AllowedMentions(users=True, roles=False, replied_user=True, everyone=False)

bot = commands.Bot(
    command_prefix=config.get("command_prefix", "!"),
    case_insensitive=True,
    intents=intents,
    help_command=None,
    allowed_mentions=am,
)


@bot.event
async def on_ready():
    logging.info(f"Bot connected as {bot.user.name}")

    if text := config.get("initial_activity"):
        output = Template(text).substitute(domain=config.get("domain"))

        await bot.change_presence(activity=Game(name=output))


async def main(token):
    async with bot:
        await bot.load_extension("bot.cogs.osu")
        await bot.start(token)
