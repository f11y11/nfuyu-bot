import yaml

from discord.mentions import AllowedMentions
from discord.ext import commands
from discord.flags import Intents

intents = Intents.all()
intents.presences = False

stream = open('config.yml', 'r')
config = yaml.safe_load(stream)
config: dict

am = AllowedMentions(users=True, roles=False, replied_user=True, everyone=False)

bot = commands.Bot(command_prefix=config.get('command_prefix', '!'),
                   case_insensitive=True,
                   intents=intents,
                   help_command=None,
                   allowed_mentions=am)


@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user.name}')


async def main(token):
    async with bot:
        await bot.load_extension("bot.cogs.osu")
        await bot.start(token)
