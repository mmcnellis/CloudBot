import json
import urllib.request

from cloudbot import hook

burl = "http://barnivore.com/beer.json"
wurl = "http://barnivore.com/wine.json"
lurl = "http://barnivore.com/liquor.json"


def beer_update():
    response = urllib.request.urlopen(burl)
    data = json.loads(response.read())
    with open('barnbeer.txt', 'w') as outfile:
        json.dump(data, outfile)
    return true

def wine_update():
    response = urllib.request.urlopen(wurl)
    data = json.loads(response.read())
    with open('barnwine.txt', 'w') as outfile:
        json.dump(data, outfile)
    return true

def liquor_update():
    response = urllib.request.urlopen(lurl)
    data = json.loads(response.read())
    with open('barnliquor.txt', 'w') as outfile:
        json.dump(data, outfile)
    return true

@hook.command("barnupdate")
def barnupdate():
    beer_update()
    wine_update()
    liquor_update()
    return true
