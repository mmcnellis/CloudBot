from fuzzywuzzy import fuzz
import json
import os
from pprint import pprint

import urllib.request

from cloudbot import hook

data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
suffix = '.json'
barn_path = os.path.join(data_dir, 'barn' + suffix)

burl = "http://barnivore.com/beer.json"
wurl = "http://barnivore.com/wine.json"
lurl = "http://barnivore.com/liquor.json"


@hook.command("barnupdate", autohelp=False)
def barnupdate():
# Append the json files and dump them to /data/barn.json
    with open(barn_path, 'w+') as outfile:

        response = urllib.request.urlopen(burl)
        str_beer = response.readall().decode('utf-8')
        beer = json.loads(str_beer)
        data = beer

        response = urllib.request.urlopen(wurl)
        str_wine = response.readall().decode('utf-8')
        wine = json.loads(str_wine)
        data.append(wine)

        response = urllib.request.urlopen(lurl)
        str_liquor = response.readall().decode('utf-8')
        liquor = json.loads(str_liquor)
        data.append(liquor)

        json.dump(data, outfile)

    return "Database updated."

