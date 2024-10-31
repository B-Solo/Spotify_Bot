from typing import Callable

from colorama import Fore, Style
from colorama import init as colorama_init


def colored_str_init():
    colorama_init()

def green(s):
    return f"{Fore.GREEN}{s}{Style.RESET_ALL}"

def cyan(s):
    return f"{Fore.CYAN}{s}{Style.RESET_ALL}"



class ColoredStr():

    color : Callable[[str], str]
    string: str

    def __init__(self, string, color=None):
        self.string = string
        self.color = color

    def __str__(self):
        if self.color:
            return self.color(self.string)
        return self.string
    
    def __eq__(self, other):
        if isinstance(other, str) or isinstance(other, ColoredStr):
            return self.string == other
        return False