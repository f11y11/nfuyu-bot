import logging
import humanize
import math
import time
import yaml

from datetime import datetime
from string import Template
from discord import Embed
from discord.ext import commands
from bot.bot import config
from helpers.converters import ArgumentConverter
from utils.api import *
from utils.db import users
from utils.enums import GameModes, Grades, Mods, filter_invalid_combos

domain = config.get("domain")

with open("templates.yml", "r", encoding="utf-8") as f:
    templates: dict = yaml.safe_load(f)


def get_template(cog_name, command_name: str) -> Template:
    """
    Obtain embed description from templates.yml and return it for substitution
    :return: string.Template
    :raises KeyError: No command description found for cog.command_name.
    """
    if val := templates.get(f"{cog_name}.{command_name}"):
        return Template(val)

    raise KeyError(f"No command description found for {cog_name}.{command_name}.")


def construct_avatar_url(player_id):
    """
    Returns the player avatar URL and prevents caching if enabled.
    :param int | str player_id:
    :return: str
    """
    url = f"https://a.{domain}/{player_id}"
    if not config.get("cache_avatars", True):
        return url

    return url + f"?{str(int(time.time()))}"

def parsecommand(input_str):
    """
    Returns a tuple containing the username and GameMode
    :return: tuple[str, GameModes]
    """
    gamemodes = {
        '-std': GameModes.STANDARD, 
        '-rx': GameModes.RX_STANDARD,
        '-taiko': GameModes.TAIKO,
        '-taikorx': GameModes.RX_TAIKO,
        '-ctb': GameModes.CATCH,
        '-ctbrx': GameModes.RX_CATCH,
        '-mania': GameModes.MANIA,
        '-ap': GameModes.AP_STANDARD, 
    }
    
    mode = None
    username = ''
    
    if not len(input_str) > 0:
        mode = GameModes.STANDARD
        return username, mode  
    
    tokens = input_str.split()
    for i, token in enumerate(tokens):
        if token.startswith('-'):
            mode = token
            username = ' '.join(tokens[:i])
            break

    if mode is None:
        mode = GameModes.STANDARD
        username = ' '.join(tokens)
        return username, mode

    try:
        mode = gamemodes[mode]
    except KeyError:
        mode = None
            
    return username, mode


async def get_username_and_mode(
        ctx, username: str = None, mode: GameModes = GameModes.STANDARD
):
    """
    Returns a tuple containing the username and GameMode
    :return: tuple[str, GameModes]
    :raises ValueError: Set your username using **!setuser**.
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


class Cog(commands.Cog, name="osu!"):
    def __init__(self, bot):
        self.bot = bot
        logging.info(f"Cog: {self.qualified_name} loaded")

    def cog_unload(self):
        logging.info(f"Cog: {self.qualified_name} unloaded")

    @commands.command()
    async def setuser(self, ctx, *, username):
        users[str(ctx.author.id)] = username
        await ctx.send(
            get_template(self.qualified_name, "setuser").substitute(username=username)
        )

    @commands.command()
    async def rs(self, ctx, *, parameters = ''):
        user, mode = parsecommand(parameters)
        
        if mode == None:
            return await ctx.send("Invalid game mode, please use any of the follow arguments: -std | -rx | -ap | -taiko | -taikorx | -ctb | -ctbrx | -mania")
        if not len(user):
            with open('users.json', 'r') as f:
                users: dict = json.loads(f.read())
                user = users.get(str(ctx.author.id))
        if not user:
            return await ctx.send("Set your username using **!setuser**.")
            
        data = await api.get(
            "get_player_scores",
            {"name": user, "scope": "recent", "limit": 1, "mode": mode.value},
        )

        player = data["player"]
        scores = data["scores"]

        if not scores:
            await ctx.send(
                f'**{player["name"]}** has no recent score in **{repr(mode)}**'
            )
        else:
            score = data["scores"][0]
            beatmap = score["beatmap"]
            has_mods = bool(
                filter_invalid_combos(Mods(score["mods"]), score["mode"]).value
            )

            description = get_template(self.qualified_name, "rs").substitute(
                grade=Grades[score["grade"]].value[1],
                pp=score["pp"],
                accuracy=score["acc"],
                score=score["score"],
                scoremaxcombo=score["max_combo"],
                beatmapmaxcombo=beatmap["max_combo"],
                n300=score["n300"],
                n100=score["n100"],
                n50=score["n50"],
                nmiss=score["nmiss"],
            )

            footer = """
            {} on osu.{}
            """.format(
                humanize.naturaltime(
                    datetime.strptime(score["play_time"], "%Y-%m-%dT%H:%M:%S")
                ).capitalize(),
                domain,
            )

            author = """
            {} [{}] {} [{:.2f}★]
            """.format(
                beatmap["title"],
                beatmap["version"],
                ("+" + repr(filter_invalid_combos(Mods(score["mods"]), score["mode"])))
                if has_mods
                else "",
                float(beatmap["diff"]),
            )

            embed = Embed(
                description=description, color=Grades[score["grade"]].value[0]
            ).set_footer(text=footer)

            embed.set_thumbnail(url=f'https://b.{domain}/thumb/{beatmap["set_id"]}.jpg')
            embed.set_author(
                name=author,
                url=f'https://osu.{domain}/beatmapsets/{beatmap["set_id"]}',
                icon_url=construct_avatar_url(player["id"]),
            )

            return await ctx.send(embed=embed)

    @commands.command(
        aliases=["mania", "ctb", "taiko", "rx", "ap", "std", "taikorx", "ctbrx"]
    )
    async def osu(self, ctx, username: str = None):
        mode: GameModes = GameModes.STANDARD

        user = username or users.get(str(ctx.author.id))

        if ctx.invoked_with == "rx":
            mode = GameModes.RX_STANDARD
        if ctx.invoked_with == "ap":
            mode = GameModes.AP_STANDARD
        if ctx.invoked_with == "std" or ctx.invoked_with == "osu":
            mode = GameModes.STANDARD
        if ctx.invoked_with == "taiko":
            mode = GameModes.TAIKO
        if ctx.invoked_with == "taikorx":
            mode = GameModes.RX_TAIKO
        if ctx.invoked_with == "ctb":
            mode = GameModes.CATCH
        if ctx.invoked_with == "ctbrx":
            mode = GameModes.RX_CATCH
        if ctx.invoked_with == "mania":
            mode = GameModes.MANIA

        data = await api.get(
            "get_player_info",
            params={
                "name": user,
                "scope": "all",
            },
        )

        player = data["player"]["info"]
        stats = data["player"]["stats"][str(mode.value)]

        def get_level_score(level):
            if level <= 100:
                if level > 1:
                    return math.floor(
                        5000
                        / 3
                        * (4 * math.pow(level, 3) - 3 * math.pow(level, 2) - level)
                        + math.floor(1.25 * math.pow(1.8, level - 60))
                    )
                return 1
            return 26931190829 + 100000000000 * (level - 100)

        def get_level(score):
            i = 1
            while True:
                lscore = get_level_score(i)
                if score < lscore:
                    return i - 1
                i += 1

        description = get_template(self.__cog_name__, "osu").substitute(
            rank=stats["rank"],
            country=player["country"].upper(),
            countryrank=stats["country_rank"],
            level=get_level(stats["tscore"]),
            pp=stats["pp"],
            playcount=stats["plays"],
            emoji_xh=Grades["XH"].value[1],
            xh_count=stats["xh_count"],
            emoji_x=Grades["X"].value[1],
            x_count=stats["x_count"],
            emoji_sh=Grades["SH"].value[1],
            sh_count=stats["sh_count"],
            emoji_s=Grades["S"].value[1],
            s_count=stats["s_count"],
            emoji_a=Grades["A"].value[1],
            a_count=stats["a_count"],
        )

        embed = Embed(
            description=description,
            color=ctx.author.color,
        )

        embed.set_author(
            name=f'{repr(mode)} Profile for {player["name"]}',
            url=f'https://osu.{domain}/u/{player["id"]}',
            icon_url=f'https://osu.{domain}/static/images/flags/{player["country"].upper()}.png',
        )
        embed.set_thumbnail(url=construct_avatar_url(player["id"]))

        return await ctx.send(embed=embed)

    @commands.command(aliases=["lb"])
    async def leaderboard(self, ctx, *, mode: ArgumentConverter = GameModes.STANDARD):
        mode: GameModes

        data = await api.get(
            "get_leaderboard",
            params={
                "mode": mode.value,
                "sort": "pp",
                "limit": 10,
            },
        )

        description = "\n".join(
            [
                get_template(self.qualified_name, "leaderboard").substitute(
                    rank=rank, name=player["name"], pp=player["pp"]
                )
                for rank, player in enumerate(data["leaderboard"], 1)
            ]
        )

        embed = Embed(description=description, color=1167239)

        embed.set_author(
            name=f"{repr(mode)} PP Leaderboard",
            icon_url="https://" + domain + "/static/favicon/favicon.ico",
        )
        embed.set_footer(text=f"osu.{domain}")

        await ctx.send(embed=embed)

    @commands.command()
    async def stats(self, ctx):
        try:
            response = await api.get("get_player_count")
        except ValueError:
            return await ctx.send(
                embed=Embed(description="Server unreachable.", color=0x00FF00)
            )
        else:
            counts = response["counts"]

            description = get_template(self.qualified_name, "stats").substitute(
                registered=counts["total"],
                online=counts["online"],
            )

            embed = Embed(description=description, color=0x00FF00)
            embed.set_thumbnail(url="https://" + domain + "/favicon.ico")
            embed.set_footer(text=f"api.{domain}")

            await ctx.send(embed=embed)

    @commands.command(
        aliases=[
            "rxtop",
            "aptop",
            "stdtop",
            "taikotop",
            "taikorxtop",
            "ctbtop",
            "ctbrxtop",
            "maniatop",
        ]
    )
    async def osutop(self, ctx, username: str = None):
        mode: GameModes = GameModes.STANDARD

        user = username or users.get(str(ctx.author.id))

        if ctx.invoked_with == "rxtop":
            mode = GameModes.RX_STANDARD
        if ctx.invoked_with == "aptop":
            mode = GameModes.AP_STANDARD
        if ctx.invoked_with == "stdtop" or ctx.invoked_with == "osutop":
            mode = GameModes.STANDARD
        if ctx.invoked_with == "taikotop":
            mode = GameModes.TAIKO
        if ctx.invoked_with == "taikorxtop":
            mode = GameModes.RX_TAIKO
        if ctx.invoked_with == "ctbtop":
            mode = GameModes.CATCH
        if ctx.invoked_with == "ctbrxtop":
            mode = GameModes.RX_CATCH
        if ctx.invoked_with == "maniatop":
            mode = GameModes.MANIA

        data = await api.get(
            "get_player_scores",
            params={"name": user, "scope": "best", "limit": 5, "mode": mode.value},
        )

        user_data = await api.get(
            "get_player_info",
            params={
                "name": user,
                "scope": "all",
            },
        )

        player = user_data["player"]["info"]
        # player is returned on /get_player_scores, but it does not include the country data
        # consider using `player = data["player"]` if country is not necessary.

        description = (
            "\n".join(
                [
                    get_template(self.qualified_name, "osutop").substitute(
                        rank=rank,
                        map=score["beatmap"]["title"],
                        difficulty=score["beatmap"]["version"],
                        mods=repr(
                            filter_invalid_combos(Mods(score["mods"]), mode.value)
                        ),
                        link=f"https://{domain}/beatmapsets/{score['beatmap']['set_id']}",
                        stars=score["beatmap"]["diff"],
                        grade=Grades[score["grade"]].value[1],
                        pp=score["pp"],
                        accuracy=score["acc"],
                        score=score["score"],
                        scoremaxcombo=score["max_combo"],
                        beatmapmaxcombo=score["beatmap"]["max_combo"],
                        n300=score["n300"],
                        n100=score["n100"],
                        n50=score["n50"],
                        nmiss=score["nmiss"],
                    )
                    for rank, score in enumerate(data["scores"], 1)
                ]
            )
            if data["scores"]
            else f"{player['name']} does not have any top plays in **{repr(mode)}**."
        )

        embed = Embed(
            description=description,
        )

        embed.set_footer(
            text=f"On {domain}",
        )
        embed.set_author(
            name=f"Top {repr(mode)} Plays for {user}",
            icon_url=f'https://osu.{domain}/static/images/flags/{player["country"].upper()}.png',
        )
        embed.set_thumbnail(url=construct_avatar_url(player["id"]))

        await ctx.send(embed=embed)

    async def cog_command_error(self, ctx, error: Exception) -> None:
        await ctx.send(error.__cause__ or error)
        if config.get("raise_command_errors", False):
            raise error


async def setup(bot):
    await bot.add_cog(Cog(bot))
