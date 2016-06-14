import json
import urllib.request

from cloudbot import hook

burl = "http://barnivore.com/beer.json"
wurl = "http://barnivore.com/wine.json"
lurl = "http://barnivore.com/liquor.json"


def beer_update():
    response = urllib.request.urlopen(burl)
    str_response = response.readall().decode('utf-8')
    data = json.loads(str_response)
    with open('../data/barnbeer.txt', 'w') as outfile:
        json.dump(data, outfile)
    return true

def wine_update():
    response = urllib.request.urlopen(wurl)
    str_response = response.readall().decode('utf-8')
    data = json.loads(str_response)
    with open('../data/barnwine.txt', 'w') as outfile:
        json.dump(data, outfile)
    return true

def liquor_update():
    response = urllib.request.urlopen(lurl)
    str_response = response.readall().decode('utf-8')
    data = json.loads(str_response)
    with open('../data/barnliquor.txt', 'w') as outfile:
        json.dump(data, outfile)
    return true

@hook.command("barnupdate")
def barnupdate():
    beer_update()
    wine_update()
    liquor_update()
    return true
