import re

from cloudbot import hook

nick_re = re.compile("^[A-Za-z0-9_|.\-\]\[\{\}]*$", re.I)
db_ready = []


def is_valid(target, db, chan):
    """ Checks if a string is a valid IRC nick. """
    if nick_re.match(target):
        target = target.lower()
        exists = db.execute("select name from seen_user where chan = :chan and name = :name",
                            {"chan": chan, "name": target}).fetchone()
        if exists:
            return True

    return False


def is_selfhug(target, hugger):
    """ Checks if people are hugging themselves. """
    return target == hugger


def db_init(db, conn_name):
    """Check to see if the DB has the hugs table. Connection name is for caching the result per connection.
    :type db: sqlalchemy.orm.Session
    """
    global db_ready
    if db_ready.count(conn_name) < 1:
        db.execute(
            "create table if not exists hugs(chan, hugger, hugged, score INTEGER, primary key(chan, hugger, hugged))")
        db.commit()
        db_ready.append(conn_name)


@hook.command("hug", "hugs")
def hug(text, nick, action, chan, db, conn):
    """.hug <user> - give <user> a warm hug"""
    target = text.strip()

    if is_selfhug(target, nick):
        return "No"

    if not is_valid(target, db, chan):
        return "I'm not hugging your imaginary friends"

    # ready to hug
    db_init(db, conn.name)
    hugs = db.execute("select score from hugs where chan = :chan and hugger = :hugger and hugged = :hugged",
                      {'chan': chan, 'hugger': nick.lower(), 'hugged': target.lower()}).fetchone()

    score = int(hugs[0]) + 1 if hugs else 1
    db.execute("insert or replace into hugs(chan, hugger, hugged, score) values (:chan, :hugger, :hugged, :score)",
               {'chan': chan, 'hugger': nick.lower(), 'hugged': target.lower(), 'score': score})
    db.commit()

    action("leers as " + nick + " hugs " + target)


@hook.command("hugged")
def hugged(text, nick, chan, db, conn):
    """.hugged <user> - See <user>'s hug stats"""
    targett = text.strip()
    target = targett.lower()

    hugs = db.execute("select score,hugger from hugs where chan = :chan and (hugger = :target or hugged = :target)",
                      {'chan': chan, 'target': target}).fetchall()

    received = 0
    received_unique = 0
    given = 0
    given_unique = 0

    for hugg in hugs:
        if hugg[1] == target:
            given += int(hugg[0])
            given_unique += 1
        else:
            received += int(hugg[0])
            received_unique += 1

    return targett + " has hugged " + str(given_unique) + " people " + str(given) + " times and has been hugged " + str(
        received) + " times by " + str(received_unique) + " people."