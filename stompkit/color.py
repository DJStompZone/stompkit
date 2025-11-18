from collections import namedtuple
import re

hexcolor_re = re.compile(r'^#?(?:[0-9a-fA-F]{6,8}|[0-9a-fA-F]{3,4})$')

ANSICOLOR = {'black': '\x1b[30m', 'blue': '\x1b[34m', 'cyan': '\x1b[36m', 'green': '\x1b[32m', 'lightblack_ex': '\x1b[90m', 'lightblue_ex': '\x1b[94m', 'lightcyan_ex': '\x1b[96m', 'lightgreen_ex': '\x1b[92m', 'lightmagenta_ex': '\x1b[95m', 'lightred_ex': '\x1b[91m', 'lightwhite_ex': '\x1b[97m', 'lightyellow_ex': '\x1b[93m', 'magenta': '\x1b[35m', 'red': '\x1b[31m', 'reset': '\x1b[39m', 'white': '\x1b[37m', 'yellow': '\x1b[33m', 'bg_black': '\x1b[40m', 'bg_blue': '\x1b[44m', 'bg_cyan': '\x1b[46m', 'bg_green': '\x1b[42m', 'bg_lightblack_ex': '\x1b[100m', 'bg_lightblue_ex': '\x1b[104m', 'bg_lightcyan_ex': '\x1b[106m', 'bg_lightgreen_ex': '\x1b[102m', 'bg_lightmagenta_ex': '\x1b[105m', 'bg_lightred_ex': '\x1b[101m', 'bg_lightwhite_ex': '\x1b[107m', 'bg_lightyellow_ex': '\x1b[103m', 'bg_magenta': '\x1b[45m', 'bg_red': '\x1b[41m', 'bg_reset': '\x1b[49m', 'bg_white': '\x1b[47m', 'bg_yellow': '\x1b[43m', 'style_bright': '\x1b[1m', 'style_dim': '\x1b[2m', 'style_normal': '\x1b[22m', 'reset_all': '\x1b[0m'}

RESET = '\x1b[0m'

class __AnsiColor(namedtuple('AnsiColor', ", ".join(ANSICOLOR.keys()))):
    def __str__(self):
        return '\n\t'.join([f"{name}: {getattr(self, name)}" for name in self._fields])

    def __repr__(self):
        fields = ", ".join([f"{name}={getattr(self, name)!r}" for name in self._fields])
        return f"{self.__class__.__name__}({fields})"


COLOR = __AnsiColor(*list(ANSICOLOR.values()))

def colored(text, colorname, reset=True):
    if colorname not in ANSICOLOR:
        raise ValueError("Invalid color name provided")
    return f"{getattr(COLOR, colorname)}{text}{RESET if reset else ''}"

def rgb(red, green, blue):
    if not all([0 <= ea <= 5 and isinstance(ea, int) for ea in (red, green, blue)]):
        raise TypeError("red, green, and blue should be integer values between 0 and 5 (inclusive)")
    code = 16 + (red * 36) + (green * 6) + blue
    output = f'\x1b[38;5;{code}m'
    # print(f"[Debug] <rgb> {red=} {green=} {blue=} output={repr(output)}")
    return output

def _to_6cube(value: int) -> int:
    return max(0, min(5, round(value / 255 * 5)))


def hexcolor_to_8bit(hexcolor: str) -> str:
    # print(f"[Debug] <hexcolor_to_8bit> {hexcolor=}")
    if not hexcolor_re.fullmatch(hexcolor):
        raise ValueError("Invalid hex color!")
    s = hexcolor.lstrip("#").lower()
    if len(s) in (3, 4):
        s = "".join(ch * 2 for ch in s)
    r_255 = int(s[0:2], 16)
    g_255 = int(s[2:4], 16)
    b_255 = int(s[4:6], 16)
    # print(f"[Debug] <hexcolor_to_8bit> {r_255=} {g_255=} {b_255=}")
    r = _to_6cube(r_255)
    g = _to_6cube(g_255)
    b = _to_6cube(b_255)
    return rgb(r, g, b)

def colored_hex(text, hexcolor, reset=True):
    return f"{hexcolor_to_8bit(hexcolor)}{text}{RESET if reset else ''}"

def colored_rgb(text, red, green, blue, reset=True):
    # print(f"[Debug] <colored_rgb> {red=} {green=} {blue=} {text=} {RESET=}")
    return f"{rgb(red, green, blue)}{text}{RESET if reset else ''}"