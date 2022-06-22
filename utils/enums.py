import functools

from enum import Enum, IntFlag, unique
from discord import Color

class Grades(Enum):
    F = (Color.from_rgb(176, 12, 26), '<:F_:988562882277040198>')
    D = (Color.from_rgb(176, 12, 26), '<:dRank:988562735560294400>')
    C = (Color.from_rgb(150, 38, 255), '<:cRank:988562575748915200>')
    B = (Color.from_rgb(38, 139, 255), '<:bRank:988562475672825906>')
    A = (Color.from_rgb(46, 204, 113), '<:aRank:988562409067253810>')
    S = (Color.from_rgb(235, 203, 42), '<:sRank:988562305908363275>')
    X = (Color.from_rgb(235, 203, 42), '<:ss:988562214883581992>')
    SH = (Color.from_rgb(219, 219, 219), '<:silvers:988561962835251230>')
    XH = (Color.from_rgb(219, 219, 219), '<:silverss:988562044104093756>')

@unique
class Mods(IntFlag):
    NOMOD = 0
    NOFAIL = 1 << 0
    EASY = 1 << 1
    TOUCHSCREEN = 1 << 2  # old: 'NOVIDEO'
    HIDDEN = 1 << 3
    HARDROCK = 1 << 4
    SUDDENDEATH = 1 << 5
    DOUBLETIME = 1 << 6
    RELAX = 1 << 7
    HALFTIME = 1 << 8
    NIGHTCORE = 1 << 9
    FLASHLIGHT = 1 << 10
    AUTOPLAY = 1 << 11
    SPUNOUT = 1 << 12
    AUTOPILOT = 1 << 13
    PERFECT = 1 << 14
    KEY4 = 1 << 15
    KEY5 = 1 << 16
    KEY6 = 1 << 17
    KEY7 = 1 << 18
    KEY8 = 1 << 19
    FADEIN = 1 << 20
    RANDOM = 1 << 21
    CINEMA = 1 << 22
    TARGET = 1 << 23
    KEY9 = 1 << 24
    KEYCOOP = 1 << 25
    KEY1 = 1 << 26
    KEY3 = 1 << 27
    KEY2 = 1 << 28
    SCOREV2 = 1 << 29
    MIRROR = 1 << 30

    @functools.cache
    def __repr__(self) -> str:
        if self.value == Mods.NOMOD:
            return "NM"

        mod_str = []
        _dict = mod2modstr_dict  # global

        for mod in Mods:
            if self.value & mod:
                mod_str.append(_dict[mod])

        return "".join(mod_str)

mod2modstr_dict = {
    Mods.NOFAIL: "NF",
    Mods.EASY: "EZ",
    Mods.TOUCHSCREEN: "TD",
    Mods.HIDDEN: "HD",
    Mods.HARDROCK: "HR",
    Mods.SUDDENDEATH: "SD",
    Mods.DOUBLETIME: "DT",
    Mods.RELAX: "RX",
    Mods.HALFTIME: "HT",
    Mods.NIGHTCORE: "NC",
    Mods.FLASHLIGHT: "FL",
    Mods.AUTOPLAY: "AU",
    Mods.SPUNOUT: "SO",
    Mods.AUTOPILOT: "AP",
    Mods.PERFECT: "PF",
    Mods.FADEIN: "FI",
    Mods.RANDOM: "RN",
    Mods.CINEMA: "CN",
    Mods.TARGET: "TP",
    Mods.SCOREV2: "V2",
    Mods.MIRROR: "MR",
    Mods.KEY1: "1K",
    Mods.KEY2: "2K",
    Mods.KEY3: "3K",
    Mods.KEY4: "4K",
    Mods.KEY5: "5K",
    Mods.KEY6: "6K",
    Mods.KEY7: "7K",
    Mods.KEY8: "8K",
    Mods.KEY9: "9K",
    Mods.KEYCOOP: "CO",
}


class GameModes(Enum):
    OSU = 0
    TAIKO = 1
    CTB = 2
    MANIA = 3
