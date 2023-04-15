import math
import humanize
import logging

from datetime import datetime
from discord.ext import commands
from discord import Embed
from bot.bot import config
from helpers.converters import ArgumentConverter
from utils.api import *
from utils.enums import GameModes, Grades, Mods, filter_invalid_combos
from utils.db import users

DEBUG: bool = config.get('debug')
domain = config.get('domain')


async def get_username_and_mode(ctx, username: str = None, mode: GameModes = GameModes.STANDARD):
    """
    Returns a tuple containing the username and GameMode
    :return: tuple[str, GameModes]
    :raises: ValueError
    """
    if username:
        try:
            _mode = await ArgumentConverter().convert(ctx, username)
        except ValueError:
            pass
        else:
            mode = _mode
            username = None

    user = username or users.get(str(ctx.author.id))

    if not user and not username:
        raise ValueError("Set your username using **!setuser**.")
    else:
        return user, mode


class Cog(commands.Cog, name='osu!'):
    def __init__(self, bot):
        self.bot = bot
        logging.info(f'Cog: {self.qualified_name} loaded')

    def cog_unload(self):
        logging.info(f'Cog: {self.qualified_name} unloaded')

    @commands.command()
    async def setuser(self, ctx, *, username):
        users.setdefault(str(ctx.author.id), username)
        await ctx.send("Username set.")

    @commands.command()
    async def rs(self, ctx, username: str = None, mode: ArgumentConverter = GameModes.STANDARD):
        mode: GameModes

        user, mode = await get_username_and_mode(ctx, username, mode)

        try:
            data = await api.get('get_player_scores', {
                "name": username or user,
                "scope": "recent",
                "limit": 1,
                "mode": mode.value
            })
        except ValueError:
            return await ctx.send("Player not found.")

        player = data["player"]
        scores = data["scores"]

        if not scores:
            await ctx.send(f'**{player["name"]}** has no recent score in **{repr(mode)}**')
        else:
            score = data["scores"][0]
            beatmap = score["beatmap"]
            has_mods = bool(filter_invalid_combos(Mods(score["mods"]), score["mode"]).value)

            description = """
            ▸ {} ▸ **{}pp ▸ {}%**
            ▸ {} ▸ x{}/{} ▸ [{}/{}/{}/{}]
            """.format(
                Grades[score["grade"]].value[1],
                score["pp"],
                score["acc"],
                score["score"],
                score["max_combo"],
                beatmap["max_combo"],
                score["n300"],
                score["n100"],
                score["n50"],
                score["nmiss"]
            )

            footer = """
            {} on osu.{}
            """.format(
                humanize.naturaltime(datetime.strptime(score["play_time"], "%Y-%m-%dT%H:%M:%S")).capitalize(),
                domain
            )

            author = """
            {} [{}] {} [{:.2f}★]
            """.format(
                beatmap["title"],
                beatmap["version"],
                ('+' + repr(filter_invalid_combos(Mods(score["mods"]), score["mode"]))) if has_mods else '',
                float(beatmap["diff"])
            )

            return await ctx.send(embed=Embed(
                description=description,
                color=Grades[score["grade"]].value[0]).set_footer(
                text=footer).set_author(name=author,
                                        url=f'https://osu.{domain}/beatmapsets/{beatmap["set_id"]}',
                                        icon_url=f'https://a.{domain}/{player["id"]}').set_thumbnail(
                url=f'https://b.{domain}/thumb/{beatmap["set_id"]}.jpg'))

    @rs.error
    async def rs_error(self, ctx, error):
        await ctx.send(error.__cause__ or error)

    @commands.command()
    async def profile(self, ctx, username: str = None, mode: ArgumentConverter = GameModes.STANDARD):
        mode: GameModes

        user, mode = await get_username_and_mode(ctx, username, mode)

        try:
            data = await api.get('get_player_info', params={
                'name': user,
                'scope': 'all',
            })
        except ValueError:
            return await ctx.send('Player not found')

        info = data["player"]["info"]
        stats = data["player"]["stats"][str(mode.value)]

        def get_level_score(level):
            if level <= 100:
                if level > 1:
                    return math.floor(5000/3*(4*math.pow(level, 3)-3*math.pow(level, 2)-level)
                                      + math.floor(1.25*math.pow(1.8, level-60)))
                return 1
            return 26931190829 + 100000000000 * (level - 100)

        def get_level(score):
            i = 1
            while True:
                lscore = get_level_score(i)
                if score < lscore:
                    return i - 1
                i += 1

        # replace description with this to replace grade emojis with text
        description = """
        ▸ **Rank:** #%s (%s#%s)\n▸ **Level:** %s
        ▸ **PP:** %s\n▸ **Playcount:** %s\n▸ **Ranks:** %s `%s` %s `%s` %s `%s` %s `%s` %s `%s`
        """ % (
            stats["rank"],
            info["country"].upper(),
            stats["country_rank"],
            get_level(stats["tscore"]),
            stats["pp"],
            stats["plays"],
            Grades["XH"].value[1],
            stats["xh_count"],
            Grades["X"].value[1],
            stats["x_count"],
            Grades["SH"].value[1],
            stats["sh_count"],
            Grades["S"].value[1],
            stats["s_count"],
            Grades["A"].value[1],
            stats["a_count"]
        )

        """
        ▸ **Rank:** #%s (%s#%s)\n▸ **Level:** %s
        ▸ **PP:** %s\n▸ **Playcount:** %s\n▸ **Ranks:** **XH** `%s` **X** `%s` **SH** `%s` **S** `%s` **A** `%s`
        """ % (
            stats["rank"],
            info["country"].upper(),
            stats["country_rank"],
            get_level(stats["tscore"]),
            stats["pp"],
            stats["plays"],
            stats["xh_count"],
            stats["x_count"],
            stats["sh_count"],
            stats["s_count"],
            stats["a_count"]
        )

        return await ctx.send(embed=Embed(
            description=description,
            color=ctx.author.color,
            )
            .set_author(
                name=f'{repr(mode)} Profile for {info["name"]}',
                url=f'https://osu.{domain}/u/{info["id"]}',
                icon_url=f'https://osu.{domain}/static/images/flags/{info["country"].upper()}.png')
            .set_thumbnail(url=f'https://a.{domain}/{info["id"]}'))

    @profile.error
    async def profile_error(self, ctx, error):
        return await ctx.send(error.__cause__ or error)

    @commands.command(aliases=['lb'])
    async def leaderboard(self, ctx, *, mode: ArgumentConverter = GameModes.STANDARD):
        mode: GameModes

        data = await api.get('get_leaderboard', params={
            'mode': mode.value,
            'sort': 'pp',
            'limit': 10,
        })

        description = '\n'.join([f'▸ **#{rank}** {player["name"]}: {player["pp"]}' for
                                 rank, player in enumerate(data["leaderboard"], 1)])

        await ctx.send(embed=Embed(
                    description=description,
                    color=1167239
                ).set_author(
                    name=f'{repr(mode)} PP Leaderboard', icon_url='https://'+domain+'/favicon.ico'
                )
                .set_footer(text=f'osu.{domain}')
              )

    @leaderboard.error
    async def leaderboard_error(self, ctx, error):
        return await ctx.send(error.__cause__ or error)

    @commands.command()
    async def stats(self, ctx):

        try:
            response = await api.get('get_player_count')
        except ValueError:
            return await ctx.send(embed=Embed(
                description='Server unreachable.',
                color=0x00ff00
            ))
        else:

            counts = response['counts']

            description = f"""
            ▸ **Registered Users:** {counts['total']}\n▸ **Currently Playing:** {counts['online']}\n
            """

            embed = Embed(
                description=description,
                color=0x00ff00
            )\
                .set_thumbnail(url='https://'+domain+'/favicon.ico')\
                .set_footer(text=f'api.{domain}')

            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Cog(bot))
