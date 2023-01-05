from typing import Union
from discord.ext.commands import Converter

from utils.enums import GameModes, Mods

__all__ = (
    'ArgumentConverter',
)

game_modes = {
    'osu': GameModes.STANDARD,
    'std': GameModes.STANDARD,
    'taiko': GameModes.STANDARD,
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

         # getting no game mode specific mode flags out of the way
        if arg == '-rx': return GameModes.RX_STANDARD
        if arg == '-ap': return GameModes.AP_STANDARD
        

        if len(arguments) == 1:
            if arg in game_modes: return game_modes[arg]
        
        # multiple arguments, expecting 2 but more are welcome
        if arguments[0] in game_modes:
            # second argument is likely a mod
            if arguments[1] in ['-rx', '-ap']:
                if arguments[1] == '-rx':
                    if arguments[0] in rx_modes:
                        return rx_modes[arguments[0]]
                    else:
                        raise ValueError('This game mode does not support RX')

                if arguments[1] == '-ap':
                    if arguments[0] in ap_modes:
                        return ap_modes[arguments[0]]
                    else:
                        raise ValueError('This game mode does not support AP')
            else:
                raise ValueError('Unrecognized mod flag')
        else:
            raise ValueError('Invalid game mode and/or mod')
    
