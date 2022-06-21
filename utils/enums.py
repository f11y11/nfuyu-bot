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
    NM = 0
    NF = 1 << 0
    EZ = 1 << 1
    TD = 1 << 2
    HD = 1 << 3
    HR = 1 << 4
    SD = 1 << 5
    DT = 1 << 6
    RX = 1 << 7
    HT = 1 << 8
    NC = 1 << 9
    FL = 1 << 10
    AU = 1 << 11
    SO = 1 << 12
    AP = 1 << 13
    PF = 1 << 14
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

    @property
    def appended(self):
        print(self.numerator)
        x = ''
        for m in Mods:
            if self & m:
                x += str(m.name)

        return x

class GameModes(Enum):
    OSU = 0
    TAIKO = 1
    CTB = 2
    MANIA = 3