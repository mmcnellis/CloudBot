"""
Various small features.
"""

from cloudbot import hook


@hook.command
def scarybon():
    return "☻"


@hook.command
def scaryboff():
    return "☺"


@hook.command
def b12(text, action):
    action("hands " + text + " a bottle of B12")
