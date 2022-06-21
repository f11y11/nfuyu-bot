from discord.ext import commands
from utils.sql import execute

class Cog(commands.Cog, name='Query Executor'):
    def __init__(self, bot):
        self.bot = bot
        print(f'Cog: {self.qualified_name} loaded')

    def cog_unload(self):
        print(f'Cog: {self.qualified_name} unloaded')

    @commands.is_owner()
    @commands.command()
    async def q(self, ctx, *, query: str):
        return await ctx.send(execute(query, limit=2000))

    @q.error
    async def q_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            return await ctx.send('You are not allowed to use this command.')
        return await ctx.send(error)

def setup(bot):
    bot.add_cog(Cog(bot))
