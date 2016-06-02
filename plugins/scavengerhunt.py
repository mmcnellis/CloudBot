import asyncio
import codecs
import json
import os

from cloudbot import hook


@hook.on_start()
def load_items(bot):
    global items

    with codecs.open(os.path.join(bot.data_dir, "scavengerhunt/items.json"), encoding="utf-8") as f:
        items = json.load(f)


def item_info(text):
    item = items.get(text)
    if item is None:
        return "That item is not on the list!"
    else:
        return "#" + text + " (" + ("achieve, " if item.get("type") else "find, ") + str(item.get("points")) + " points) - " \
               + item.get("objective") + ((" | " + str(item.get("info"))) if item.get("info") else "")


@asyncio.coroutine
@hook.command("ssc", autohelp=False)
def ssc(text):
    """<item number> - return information on an item"""
    if not text:
        return "The summer scavenger hunt is organised by /u/lnfinity every year. Check out /r/SummerScavengerHunt on reddit."

    try:
        int(text)
        return item_info(text)
    except ValueError:
        return "That item is not on the list!"
