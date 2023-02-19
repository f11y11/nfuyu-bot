import math
import humanize
import json

from datetime import datetime
from discord.ext import commands
from discord import Embed, Member
from bot.bot import config
from typing import Optional, Union
from helpers.converters import ArgumentConverter
from helpers.dndict import DNDict
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
    async def rs(self, ctx, *, mode: ArgumentConverter = GameModes.STANDARD):
        with open('users.json', 'r') as f: 
            users: dict = json.loads(f.read())
            user = users.get(str(ctx.author.id))
        if not user:
            return await ctx.send('Set your username using **!setuser**.')


        api_response = await req('api', 'v1/get_player_scores', 'GET', params={
            'name': user,
            'scope': 'recent',
            'limit': 1,
            'mode': mode.value
        })

        if api_response[1]: # success
            res = api_response[0]
            player = DNDict(res['player'])

            if not res['scores']:
                return await ctx.send(f'**{player.name}** has no recent score in **{repr(mode)}**')

            score = DNDict(res['scores'][0])
            map = DNDict(score.beatmap)

            return await ctx.send(embed=Embed(
                description = 
                f'▸ {Grades[score.grade].value[1]} ▸ **{score.pp}pp ▸ {score.acc}%**\n▸ {score.score} ▸ x{score.max_combo}/{map.max_combo} ▸ [{score.n300}/{score.n100}/{score.n50}/{score.nmiss}]',
                color = Grades[score.grade].value[0],
                ).set_footer(text=f'{humanize.naturaltime(datetime.strptime(score.play_time,"%Y-%m-%dT%H:%M:%S")).capitalize()} on osu.{domain}')
                .set_author(name=f'{map.title} [{map.version}] +{repr(filter_invalid_combos(Mods(score.mods), score.mode))} [{float(map.diff):.2f}★]', url=f'https://osu.{domain}/beatmapsets/{map.set_id}', icon_url=f'https://a.{domain}/{player.id}')
                .set_thumbnail(url=f'https://b.{domain}/thumb/{map.set_id}.jpg')
                )
        else:
            return await ctx.send('A server error occured.' if not DEBUG else str(api_response[0])[:2000])

    @rs.error
    async def rs_error(self, ctx, error):
        return await ctx.send(error.__cause__ or error)

    @commands.command()
    async def profile(self, ctx, *, mode: ArgumentConverter = GameModes.STANDARD):
        with open('users.json', 'r') as f: 
            users: dict = json.loads(f.read())
            user = users.get(str(ctx.author.id))
        if not user:
            return await ctx.send('Set your username using **!setuser**.')

        api_response = await req('api', 'v1/get_player_info', 'GET', params={
            'name': user,
            'scope': 'all',
        })
        if api_response[1]: # success
            res = api_response[0]

            info = DNDict(res['player']['info'])
            stats = DNDict(res['player']['stats'][str(mode.value)])

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
                f'▸ **Rank:** #{stats.rank} ({info.country.upper()}#{stats.country_rank})\n▸ **Level:** {getlevel(stats.tscore)}\n▸ **PP:** {stats.pp}\n▸ **Playcount:** {stats.plays}\n▸ **Ranks:** {Grades.XH.value[1]}`{stats.xh_count}`{Grades.X.value[1]}`{stats.x_count}`{Grades.SH.value[1]}`{stats.sh_count}`{Grades.S.value[1]}`{stats.s_count}`{Grades.A.value[1]}`{stats.a_count}`',
                color = ctx.author.color,
                )
                .set_author(name=f'{repr(mode)} Profile for {info.name}', url=f'https://osu.{domain}/u/{info.id}', icon_url=f'https://osu.{domain}/static/images/flags/{info.country.upper()}.png')
                .set_thumbnail(url=f'https://a.{domain}/{info.id}')
                )
        else:
            return await ctx.send('Player not found or a server error occured.' if not DEBUG else str(api_response[0])[:2000])

    @profile.error
    async def profile_error(self, ctx, error):
        return await ctx.send(error.__cause__ or error)

    @commands.command(aliases=['lb'])
    async def leaderboard(self, ctx, *, mode: ArgumentConverter = GameModes.STANDARD):
        api_response = await req('api', 'v1/get_leaderboard', 'GET', params={
            'mode': mode.value,
            'sort': 'pp',
            'limit': 10,
        })

        if api_response[1]:
            lb_str = '\n'.join([f'▸ **#{rank}** {player["name"]}: {player["pp"]}' for rank, player in enumerate(api_response[0]['leaderboard'], 1)])

            await ctx.send(embed=Embed(
                        description=lb_str,
                        color=1167239
                    ).set_author(
                        name=f'{repr(mode)} PP Leaderboard',
                    )
                    .set_footer(text=f'osu.{domain}')
                  )
        else:
            return await ctx.send('A server error occured.' if not DEBUG else str(api_response[0])[:2000])

    @leaderboard.error
    async def leaderboard_error(self, ctx, error):
        return await ctx.send(error.__cause__ or error)

async def setup(bot):
    await bot.add_cog(Cog(bot))
