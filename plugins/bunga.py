import random

from cloudbot import hook


@hook.command("grr", "grrr", autohelp=False)
def grr():
    """bunga bunga bunga!"""
    return ":o"


@hook.command("bunga", autohelp=False)
def bunga():
    """bunga bunga bunga!"""
    return random.choice(("grr", "whaaa", ":o"))

@hook.command("hostmask", autohelp=False)
def host(event):
    return event.mask
