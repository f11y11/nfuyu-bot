from typing import Union
from discord.ext.commands import Converter

from utils.enums import GameModes, Mods

__all__ = (
    'ArgumentConverter',
)

game_modes = {
    'osu': GameModes.STANDARD,
    'std': GameModes.STANDARD,
    'taiko': GameModes.TAIKO,
    'catch': GameModes.CATCH,
    'ctb': GameModes.CATCH,
    'mania': GameModes.MANIA,
}
rx_modes = {
    'osu': GameModes.RX_STANDARD,
    'std': GameModes.RX_STANDARD,
    'taiko': GameModes.RX_TAIKO,
    'catch': GameModes.RX_CATCH,
    'ctb': GameModes.RX_CATCH,
}
ap_modes = {
    'osu': GameModes.AP_STANDARD,
    'std': GameModes.AP_STANDARD
}


class ArgumentConverter(Converter):
    """
    Converts an argument into game mode or mod depending on it's value
    """

    async def convert(self, ctx, arg) -> GameModes:
        """
        arg will hold all the arguments specified by the user
        this, because of the game modes rely on the specified mod
        such as RX; being Gamemodes.RX_STANDARD instead of Gamemodes.STANDARD
        """

        arguments = arg.split()

        if not len(arguments):
            raise ValueError('No arguments were specified')

        if arg == '-rx':
            return GameModes.RX_STANDARD
        if arg == '-ap':
            return GameModes.AP_STANDARD
        if arg == '-std':
            return GameModes.STANDARD
        if arg == '-vn':
            return GameModes.STANDARD
        if arg == '-taiko':
            return GameModes.TAIKO
        if arg == '-taikorx':
            return GameModes.RX_TAIKO
        if arg == '-ctb':
            return GameModes.CATCH
        if arg == '-ctbrx':
            return GameModes.RX_CATCH
        if arg == '-mania':
            return GameModes.MANIA

        if len(arguments) == 1:
            if arg in game_modes:
                return game_modes[arg]
        else:
            raise ValueError('Invalid game mode and/or mod')
