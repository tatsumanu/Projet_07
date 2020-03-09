import re
import json
import wikipedia
import requests
from random import choice
from config import GOOGLE_MAP_API_KEY


class Answer:

    """ The user's request creates an instance of this class. The request is
    cleaned a little bit by managing punctuation, case, and compared to a
    list of commonly used words. The result is a string returned by searching
    method. """
    def __init__(self, question):
        self.question = question
        self.answer = []
        try:
            with open('stop.json') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {}

    def searching(self):
        total = re.findall(r'[a-zA-Zéèùàêô]*', self.question)
        verb = re.findall(r'[a-zA-Z]*er', self.question)
        for elt in total:
            if elt != "":
                if elt not in verb:
                    if elt.lower() not in self.data:
                        self.answer.append(elt)
        return ' '.join(self.answer)


class Map:

    """ The string returned by Answer class is sent to the google map
    API. A json containing coordinates and an address is received and
    returned to the next step. """
    def __init__(self, data):
        self.data = data
        self.geo_resp = {}

    def geo_search(self):
        url = "https://maps.googleapis.com/maps/api/geocode/json?"
        parameters = {
            'address': self.data,
            'key': GOOGLE_MAP_API_KEY,
            'language': 'FR',
            'region': 'FR'
        }
        ask = requests.get(url, params=parameters)
        self.geo_resp = ask.json()["results"]
        return self.geo_resp


class Wiki:

    """ Usefull stuff is taken in the google map response and then passed
    to the wikipedia API in order to retrieve the informations needed
    for GrandPy to answer. """
    def __init__(self, geocode):
        try:
            self.latitude = geocode[0]["geometry"]["location"]["lat"]
            self.longitude = geocode[0]["geometry"]["location"]["lng"]
            self.address = geocode[0]["formatted_address"]
            self.lost = ""
        except IndexError:
            """ If map API returns no response, default values are provided
            to the wiki object and then returned by the application """
            self.latitude = 48.8748465
            self.longitude = 2.3504873
            self.address = 'De retour chez OpenClassrooms... '
            self.lost = """ Désolé mais quand je suis perdu, je reviens
             toujours à mon point de départ! Je ne suis qu'un robot
              après tout..."""
        self.response = {}
        self.some_bargain = ["C'est ici mon petit... ",
                             "Bien sûr mon petit, voilà l'adresse... ",
                             "Hum, voyons, c'est situé là je crois... ",
                             "Oh, très intéressant oui! C'est situé... ",
                             "Rrrrr... Pardon? Qu'y a-t'il mon poussin? "]
        self.other_blabla = [". Voyons, que puis-je te raconter sur cet \
            endroit ... ",
                             """. C'est un secteur intéressant!
                              Par exemple... """,
                             ". Ah je me souviens que... "]
        wikipedia.set_lang('fr')

    def asking(self):
        self.response["coord"] = {'lat': self.latitude, 'lng': self.longitude}
        if not self.lost:
            try:
                self.response["localize"] = wikipedia.geosearch(self.latitude,
                                                                self.longitude)
                self.response["answer"] = choice(self.some_bargain) + \
                    self.address
                title = choice(self.response["localize"])
                page = wikipedia.page(title=title)
                self.response["environment"] = choice(self.other_blabla) + \
                    page.summary
            except (wikipedia.exceptions.PageError, IndexError):
                self.response['environment'] = """. Je suis désolé mon petit,
                 ma mémoire me fait défaut et je n'ai rien à te dire à ce
                  sujet..."""
        else:
            self.response["answer"] = self.address
            self.response["environment"] = self.lost
        return self.response
