import math
import humanize
import json

from datetime import datetime
from discord.ext import commands
from discord import Embed, Member
from bot.bot import config
from typing import Optional, Union
from helpers.dictobj import DNDict
from utils.api import req
from utils.enums import GameModes, Grades, Mods, filter_invalid_combos

DEBUG : bool = config.get('debug')
domain = config.get('domain')

class Cog(commands.Cog, name='osu!'):
    def __init__(self, bot):
        self.bot = bot
        print(f'Cog: {self.qualified_name} loaded')

    def cog_unload(self):
        print(f'Cog: {self.qualified_name} unloaded')

    @commands.command()
    async def setuser(self, ctx, *, username):
        with open('users.json', 'r') as f:
            users = json.loads(f.read())

        users[str(ctx.author.id)] = username

        with open('users.json', 'w') as f:
            f.write(json.dumps(users, indent=4))

        await ctx.send('Success.')

    @commands.command()
    async def rs(self, ctx, *, user: Optional[Union[Member, str]]):
        with open('users.json', 'r') as f: users: dict = json.loads(f.read())

        if isinstance(user, Member):
            # if a discord.Member is specified, get their username from users.json
            user = users.get(str(user.id)) # get from json

        if not user: # if user is not discord.Member or not specified
            user = users.get(str(ctx.author.id)) # get from json
            if not user: # not found in json, at this point user is unreachable by any means
                return await ctx.send('Specify a username | Link your username to your account using !setuser')

        api_response = await req('api', 'get_player_scores', 'GET', params={
            'name': user,
            'scope': 'recent',
            'mods': 0,
            'limit': 1
        })

        if api_response[1]: # success
            res = api_response[0]
            score = DNDict(res['scores'][0])
            player = DNDict(res['player'])
            map = DNDict(score.beatmap)

            return await ctx.send(embed=Embed(
                description = 
                f'''
                ▸ {Grades[score.grade].value[1]} ▸ **{score.pp}pp ▸ {score.acc}%**
                ▸ {score.score} ▸ x{score.max_combo}/{map.max_combo} ▸ [{score.n300}/{score.n100}/{score.n50}/{score.nmiss}]
                ''',
                color = Grades[score.grade].value[0],
                ).set_footer(text=f'{humanize.naturaltime(datetime.strptime(score.play_time,"%Y-%m-%dT%H:%M:%S")).capitalize()} on osu.{domain}')
                .set_author(name=f'{map.title} [{map.version}] +{repr(filter_invalid_combos(Mods(score.mods), score.mode))} [{float(map.diff):.2f}★]', url=f'https://osu.{domain}/beatmapsets/{map.set_id}', icon_url=f'https://a.{domain}/{player.id}')
                .set_thumbnail(url=f'https://b.{domain}/thumb/{map.set_id}.jpg')
                )
        else:
            return await ctx.send('A server error occured.' if not DEBUG else str(api_response[0])[:2000])

    @rs.error
    async def q_error(self, ctx, error):
        return await ctx.send(error)

    @commands.command(aliases=['taiko', 'ctb', 'mania'])
    async def osu(self, ctx, *, user: Optional[Union[Member, str]]):
        with open('users.json', 'r') as f: users: dict = json.loads(f.read())

        if isinstance(user, Member):
            # if a discord.Member is specified, get their username from users.json
            user = users.get(str(user.id)) # get from json

        if not user: # if user is not discord.Member or not specified
            user = users.get(str(ctx.author.id)) # get from json
            if not user: # not found in json, at this point user is unreachable by any means
                return await ctx.send('Specify a username | Link your username to your account using !setuser')

        api_response = await req('api', 'get_player_info', 'GET', params={
            'name': user,
            'scope': 'all',
        })
        if api_response[1]: # success
            res = api_response[0]

            info = DNDict(res['player']['info'])
            stats = DNDict(res['player']['stats'][str(GameModes[ctx.invoked_with.upper()].value)])

            def getlevelscore(level):
                if (level <= 100):
                    if (level > 1):
                        return math.floor(5000/3*(4*math.pow(level, 3)-3*math.pow(level, 2)-level) + math.floor(1.25*math.pow(1.8, level-60)))
                    return 1
                return 26931190829 + 100000000000*(level-100);
            
            def getlevel(score):
                i = 1;
                while True: 
                    lScore = getlevelscore(i)
                    if (score < lScore):
                        return i - 1
                    i+=1

            return await ctx.send(embed=Embed(
                description = 
                f'''
                ▸ **Rank:** #{stats.rank} ({info.country.upper()}#{stats.country_rank})
                ▸ **Level:** {getlevel(stats.tscore)}
                ▸ **PP:** {stats.pp}
                ▸ **Playcount:** {stats.plays}
                ▸ **Ranks:** {Grades.XH.value[1]}`{stats.xh_count}`{Grades.X.value[1]}`{stats.x_count}`{Grades.SH.value[1]}`{stats.sh_count}`{Grades.S.value[1]}`{stats.s_count}`{Grades.A.value[1]}`{stats.a_count}` 
                ''',
                color = ctx.author.color,
                )
                .set_author(name=f'osu! {GameModes[ctx.invoked_with.upper()].name.title() if not ctx.invoked_with.upper() == "OSU" else "Standard"} Profile for {info.name}', url=f'https://osu.{domain}/u/{info.id}', icon_url=f'https://osu.{domain}/static/images/flags/{info.country.upper()}.png')
                .set_thumbnail(url=f'https://a.{domain}/{info.id}')
                )
        else:
            return await ctx.send('Player not found or a server error occured.' if not DEBUG else str(api_response[0])[:2000])

    @osu.error
    async def osu_error(self, ctx, error):
        return await ctx.send(error)

    

def setup(bot):
    bot.add_cog(Cog(bot))
