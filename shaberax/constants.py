from colorama import Fore, Style, Back
from colorama.ansi import AnsiCodes


def color(text: str, ansi: AnsiCodes) -> str:
    return ansi + text + Style.RESET_ALL


ERROR = color("%(levelname)s", Back.RED)
TELEGRAM = color("TELEGRAM", Fore.BLUE)
