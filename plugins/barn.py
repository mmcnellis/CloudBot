import json
import os
import urllib.request

from cloudbot import hook

@hook.command("barnupdate", autohelp=False)
def barnupdate():
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    suffix = '.json'

    beer_path = os.path.join(data_dir, 'barnbeer' + suffix)
    wine_path = os.path.join(data_dir, 'barnwine' + suffix)
    liquor_path = os.path.join(data_dir, 'barnliquor' + suffix)

    burl = "http://barnivore.com/beer.json"
    wurl = "http://barnivore.com/wine.json"
    lurl = "http://barnivore.com/liquor.json"

# beer update
    response = urllib.request.urlopen(burl)
    str_response = response.readall().decode('utf-8')
    data = json.loads(str_response)
    with open(beer_path, 'w+') as outfile:
        json.dump(data, outfile)

# wine update
    response = urllib.request.urlopen(wurl)
    str_response = response.readall().decode('utf-8')
    data = json.loads(str_response)
    with open(wine_path, 'w+') as outfile:
        json.dump(data, outfile)

# liquor update
    response = urllib.request.urlopen(lurl)
    str_response = response.readall().decode('utf-8')
    data = json.loads(str_response)
    with open(liquor_path, 'w+') as outfile:
        json.dump(data, outfile)    

    return "Database updated."
