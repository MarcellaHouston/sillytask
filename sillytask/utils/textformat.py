"""ANSI escape sequence generating functions."""

from hashlib import sha256
from sillytask.config import Config

RESET_CODE = "\x1b[0m"
# ANSI 265 color codes that are too dark to see easy on dark screen
DARK = set(
    [
        0,
        8,
        16,
        17,
        18,
        19,
        20,
        22,
        23,
        24,
        52,
        53,
        54,
        58,
        59,
        60,
        88,
        89,
        90,
        91,
        94,
        95,
        96,
        97,
        124,
        125,
        126,
    ]
)
# Too bright to see easy on bright screen
LIGHT = set(
    [
        7,
        15,
        87,
        121,
        122,
        123,
        147,
        155,
        156,
        157,
        158,
        159,
        188,
        189,
        190,
        191,
        192,
        193,
        194,
        195,
        218,
        219,
        223,
        224,
        225,
        226,
        227,
        228,
        229,
        230,
        231,
    ]
)


def code_of(
    c: int | None = None,
    *,
    cross: bool = False,
    bold: bool = False,
    dim: bool = False,
    italic: bool = False,
) -> str:
    """Return an ANSI color sequence with color c or no color if c == 0."""
    flag_map = {
        "1": bold,
        "2": dim,
        "3": italic,
        "9": cross,
        f"38;5;{c}": c,
    }
    code = ";".join([code for code, flag in flag_map.items() if flag])
    return f"\x1b[{code}m" if code else ""


def color_hash(s: str | None) -> int:
    """Hash s into one of the colorful ANSI 256 color codes."""
    if s is None:
        return 0

    num = int(sha256(s.encode()).hexdigest(), 16) % 231
    while (Config.DARK_TERMINAL and num in DARK) or (
        not Config.DARK_TERMINAL and num in LIGHT
    ):
        s += "@"
        num = int(sha256(s.encode()).hexdigest(), 16) % 230
    return num + 1
