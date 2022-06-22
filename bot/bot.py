import os, yaml
from discord.mentions import AllowedMentions

from discord.colour import Colour
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
    await bot.wait_until_ready()
    for filename in os.listdir('./bot/cogs'):
        if filename.endswith('.py') and not filename.startswith('_'):
            bot.load_extension(('bot.cogs.' + filename[:-3]))


bot.loop.create_task(load_cogs())