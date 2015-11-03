import requests

from cloudbot import hook
from cloudbot.util import web


# @hook.command("lmgtfy", "gfy")
# def lmgtfy(text):
#     """[phrase] - gets a lmgtfy.com link for the specified phrase"""
#
#     link = "http://lmgtfy.com/?q={}".format(requests.utils.quote(text))
#
#     return web.try_shorten(link)

@hook.command("lmgtfy", "gfy", "lmdtfy", "dfy")
def lmgtfy(text):
    """[phrase] - gets a lmddgtfy.net link for the specified phrase"""

    link = "http://lmddgtfy.net//?q={}".format(requests.utils.quote(text))

    return web.try_shorten(link)