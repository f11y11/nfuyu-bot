import os, yaml, asyncio

from discord.mentions import AllowedMentions
from discord.ext import commands
from discord.flags import Intents

intents = Intents.all()
intents.presences = False
# intents.messages: used to receive commands
# intents.members: used to receive commands

stream = open('config.yml', 'r')
config = yaml.safe_load(stream)
config: dict

am = AllowedMentions(users=True, roles=False, replied_user=True, everyone=False)

bot = commands.Bot(command_prefix=config.get('command_prefix', '!'),
                   case_insensitive=True,
                   intents=intents,
                   help_command=None,
                   owner_ids=config.get('owners_ids'),
                   allowed_mentions=am)


@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user.name}')

async def load_cogs():
    await bot.load_extension("bot.cogs.osu")
    await bot.load_extension("bot.cogs.sql")
            

asyncio.run(load_cogs())

async def main(token):
    async with bot:
        await bot.start(token)
        

    
