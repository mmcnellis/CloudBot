import time
import random
import re

from cloudbot import hook

nick_re = re.compile("^[A-Za-z0-9_|.\-\]\[\{\}]*$", re.I)
db_ready = []

last_shot = {}
last_snack = {}

def db_init(db, conn_name):
    """Check to see if the DB has the rusroul table. Connection name is for caching the result per connection.
    :type db: sqlalchemy.orm.Session
    """
    global db_ready
    if db_ready.count(conn_name) < 1:
        db.execute(
            "create table if not exists rusroul(chan, nick, dead INTEGER DEFAULT 0, score INTEGER DEFAULT 0, primary key(chan, nick))")
        db.commit()
        db_ready.append(conn_name)


def is_valid(target):
    """ Checks if a string is a valid IRC nick. """
    if nick_re.match(target):
        return True
    else:
        return False


@hook.command("russianroulette", "rr", autohelp=False)
def russian_roulette(nick, chan, db, conn):
    """- Play Russian Roulette"""
    db_init(db, conn.name)
    data = db.execute("select dead, score from rusroul where chan = :chan and nick = :nick",
                      {'chan': chan, 'nick': nick.lower()}).fetchone()

    score = int(data[1]) if data else 0
    if data and int(data[0]) == 1:
        return "Been there, done that, blew your brains out. Sorry!"

    now = time.time()
    if last_shot.get(nick.lower(), 0) > (now - 300):
        return "There's a 5 minute cooldown on being an idiot."
    else:
        last_shot[nick.lower()] = now

    if random.randint(1, 6) == 6:
        db.execute("insert or replace into rusroul(chan, nick, dead, score) values (:chan, :nick, :dead, :score)",
               {'chan': chan, 'nick': nick.lower(), 'dead': 1, 'score': score})
        db.commit()
        return "Bang! " + nick + " is ded, having tempted fate a total of " + str(score) + " times."

    score = int(data[1]) + 1 if data else 1
    db.execute("insert or replace into rusroul(chan, nick, dead, score) values (:chan, :nick, :dead, :score)",
               {'chan': chan, 'nick': nick.lower(), 'dead': 0, 'score': score})
    db.commit()

    return "*Click* " + nick + " lives to die another day, having survived a total of " + str(score) + " games."


@hook.command("rrscore", "rrs", autohelp=False)
def russian_score(text, nick, chan, db, conn):
    """<nick> - Check <nick>'s russian roulette score"""
    targett = text.strip()

    if not targett:
        targett = nick

    target = targett.lower()

    if is_valid(target):
        db_init(db, conn.name)
        data = db.execute("select dead, score from rusroul where chan = :chan and nick = :nick",
                      {'chan': chan, 'nick': target}).fetchone()

        if data:
            return targett + " is " + ("dead" if int(data[0]) == 1 else "alive") + " and has survived " + \
                   str(data[1]) + " games of Russian Roulette."
        else:
            return targett + " has never shot themselves with a loaded weapon before. How curious."

    return "come again?"


@hook.command("unshoot",  permissions=["op"])
def unshoot(nick, text, chan, db, conn):
    """<nick> - reset score and death in Russian Roulette"""
    targett = text.strip()

    if not targett:
        targett = nick

    target = targett.lower()

    if is_valid(target):
        db_init(db, conn.name)
        db.execute("insert or replace into rusroul(chan, nick, dead, score) values (:chan, :nick, :dead, :score)",
               {'chan': chan, 'nick': target, 'dead': 0, 'score': 0})
        db.commit()
        return "done!"

    return "no u"


@hook.command("rrtop", autohelp=False)
def rrtop(chan, db, conn):
    """Print the 3 top Russian Roulette players"""
    db_init(db, conn.name)
    items = ""
    items = db.execute("select nick, score from rusroul where chan = :chan and dead = 0 ORDER BY score DESC ", {'chan': chan}).fetchall()
    if items:
        return "The best player is " + str(items[0][0]) + ", having survived " + str(items[0][1]) + " games of Russian Roulette."

    return "!"


def db_ddinit(db, conn_name):
    """Check to see if the DB has the dondang table. Connection name is for caching the result per connection.
    :type db: sqlalchemy.orm.Session
    """
    global db_ready
    if db_ready.count(conn_name) < 1:
        db.execute(
            "create table if not exists dondang(chan, nick, omni INTEGER DEFAULT 0, score INTEGER DEFAULT 0, primary key(chan, nick))")
        db.commit()
        db_ready.append(conn_name)


@hook.command("donutdanger", "dd", autohelp=False)
def donut_danger(nick, chan, db, conn):
    """- Play Donut Danger"""
    db_ddinit(db, conn.name)
    data = db.execute("select omni, score from dondang where chan = :chan and nick = :nick",
                      {'chan': chan, 'nick': nick.lower()}).fetchone()

    score = int(data[1]) if data else 0
    
    now = time.time()
    if last_snack.get(nick.lower(), 0) > (now - 300):
        return "There's a 5 minute cooldown on stuffing your face."
    else:
        last_snack[nick.lower()] = now

    if random.randint(1, 6) == 6:
        db.execute("insert or replace into dondang(chan, nick, omni, score) values (:chan, :nick, :omni, :score)",
               {'chan': chan, 'nick': nick.lower(), 'omni': 1, 'score': 0})
        db.commit()
        return "SCUM! " + nick + " ate an omnidonut! (" + str(score) + " donut streak over)"

    score = int(data[1]) + 1 if data else 1
    db.execute("insert or replace into dondang(chan, nick, omni, score) values (:chan, :nick, :omni, :score)",
               {'chan': chan, 'nick': nick.lower(), 'omni': 0, 'score': score})
    db.commit()

    return "YUM! " + nick + " enjoys a harmless donut. (" + str(score) + " donut streak)"


@hook.command("ddscore", "dds", autohelp=False)
def donut_score(text, nick, chan, db, conn):
    """<nick> - Check <nick>'s donut danger score"""
    targett = text.strip()

    if not targett:
        targett = nick

    target = targett.lower()

    if is_valid(target):
        db_ddinit(db, conn.name)
        data = db.execute("select omni, score from dondang where chan = :chan and nick = :nick",
                      {'chan': chan, 'nick': target}).fetchone()

        if data:
            return targett + " has been vegan for " + str(data[1]) + " donuts."
        else:
            return targett + " has never tried a donut before. How curious."

    return "come again?"

    @hook.command("ddtop", autohelp=False)
def ddtop(chan, db, conn):
    """Print the 3 top Donut Danger players"""
    db_ddinit(db, conn.name)
    items = ""
    items = db.execute("select nick, score from dondang where chan = :chan and omni = 0 ORDER BY score DESC ", {'chan': chan}).fetchall()
    if items:
        return "The best player is " + str(items[0][0]) + ", having eaten " + str(items[0][1]) + " vegan donuts in a row."

    return "!"
