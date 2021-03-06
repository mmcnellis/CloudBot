import random

import microdata
import requests
import bs4

from cloudbot import hook
from cloudbot.util import web

base_url = "http://www.cookstr.com"
search_url = base_url + "/searches?dit%5B%5D=vegan"
random_url = search_url + "&sort=created_at"

# set this to true to censor this plugin!
censor = True
phrases = [
    "EAT SOME FUCKING \x02{}\x02",
    "YOU WON'T NOT MAKE SOME FUCKING \x02{}\x02",
    "HOW ABOUT SOME FUCKING \x02{}?\x02",
    "WHY DON'T YOU EAT SOME FUCKING \x02{}?\x02",
    "MAKE SOME FUCKING \x02{}\x02",
    "INDUCE FOOD COMA WITH SOME FUCKING \x02{}\x02",
    "CLASSILY PARTAKE IN SOME FUCKING \x02{}\x02",
    "COOK UP SOME FUCKING \x02{}\x02",
    "CURE YOUR MOUTH'S POST TRAUMATIC STRESS DISORDER WITH SOME FUCKING \x02{}\x02",
    "PROCURE SOME CHILD LABOR TO COOK UP SOME FUCKING \x02{}\x02",
    "YOUR INDECISION IS FAR LESS APPETIZING THAN SOME FUCKING \x02{}\x02",
    "PROBABLY FUCK UP SOME FUCKING \x02{}\x02",
    "LESSEN YOUR MOTHER'S SHAME WITH SOME FUCKING \x02{}\x02",
    "EAT SHIT, OR IF YOU DON'T LIKE THAT, SOME FUCKING \x02{}\x02"
]

clean_key = lambda i: i.split("#")[1]


class ParseError(Exception):
    pass


def get_data(url):
    """ Uses the metadata module to parse the metadata from the provided URL """
    try:
        request = requests.get(url)
        request.raise_for_status()
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        raise ParseError(e)

    items = microdata.get_items(request.text)

    for item in items:
        if item.itemtype == [microdata.URI("http://schema.org/Recipe")]:
            return item

    raise ParseError("No recipe data found")


@hook.command(autohelp=False)
def recipe(text):
    """[term] - gets a recipe for [term], or gets a random recipe if no term is specified"""
    if not text:
        text = "salad"
    if text:
        # get the recipe URL by searching
        try:
            request = requests.get(search_url, params={'query': text.strip()})
            request.raise_for_status()
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
            return "Could not get recipe: {}".format(e)

        search = bs4.BeautifulSoup(request.text)

        # find the list of results
        result_list = search.find('div', {'class': 'found_results'})

        if result_list:
            results = result_list.find_all('div', {'class': 'recipe_result'})
        else:
            return "No results"

        # pick a random front page result
        result = random.choice(results)

        # extract the URL from the result
        url = base_url + result.find('div', {'class': 'image-wrapper'}).find('a')['href']

    else:
        # get a random recipe URL
        try:
            request = requests.get(random_url)
            request.raise_for_status()
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
            return "Could not get recipe: {}".format(e)

        url = request.url

    # use get_data() to get the recipe info from the URL
    try:
        data = get_data(url)
    except ParseError as e:
        return "Could not parse recipe: {}".format(e)

    name = data.name.strip()
    return "Try eating \x02{}!\x02 - {}".format(name, web.try_shorten(url))