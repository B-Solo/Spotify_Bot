from typing import Callable

from colorama import Fore, Style
from colorama import init as colorama_init


def colored_str_init():
    colorama_init()

def green(s):
    return f"{Fore.GREEN}{s}{Style.RESET_ALL}"

def cyan(s):
    return f"{Fore.CYAN}{s}{Style.RESET_ALL}"



def color_user_input(input_msg, color):
    """Ask for user input, which will be colored when they type

    Args:
        input_msg (str): Message to send to the user prompting the input
        color (str): A Fore color from the colorama module

    Returns:
        str: The value received from the user
    """
    x = input(f"{input_msg}{color}")
    print(f"{Style.RESET_ALL}")
    return x

class ColoredStr():
    """
    A class whose value can be get and set as a string, but on print,
    colored text is returned.
    """

    color : Callable[[str], str]
    string: str

    def __init__(self, string, color=None):
        if string:
            self.string = string
        else:
            self.string = ""
        self.color = color

    def lower(self):
        """Return the lower case string of the same colour

        Returns:
            ColoredStr: The current string, but in lowercase
        """
        return ColoredStr(self.string.lower(), self.color)

    def center(self, n):
        return ColoredStr(self.string.center(n), self.color)


    def __str__(self):
        if self.color:
            return self.color(self.string)
        return self.string

    def __eq__(self, other):
        if isinstance(other, ColoredStr):
            return self.string == other.string
        if isinstance(other, str):
            return self.string == other
        return False
