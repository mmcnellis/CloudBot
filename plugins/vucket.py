"""
Plugin implementing a subset of xkcd bucket (http://wiki.xkcd.com/irc/Bucket) functionality.
"""

import re

from cloudbot import hook

listen_re = re.compile("^((gary|vucket)(,|:)? )(?P<text>.+)", re.IGNORECASE)


@hook.regex(listen_re)
def reply(match, conn, nick, chan, message):
    text = match.group('text')

    if text.startswith("remember"):
        args = text.split(maxsplit=2)
        if len(args) > 2:
            return "kk " + args[1] + " | " + args[2]
        elif len(args) == 2:
            return "kk " + args[1]
        else:
            return "Not really"

    return "idk"
