import re
import json
import wikipedia
import requests
from random import choice


class Answer:

    def __init__(self, question):
        self.question = question
        self.answer = []
        with open('stop.json') as f:
            self.data = json.load(f)

    def searching(self):
        total = re.findall(r'[a-zA-Z]*', self.question)
        verb = re.findall(r'[a-zA-Z]*er', self.question)
        for elt in total:
            if elt != "":
                if elt not in verb:
                    if elt.lower() not in self.data:
                        self.answer.append(elt)
        return ' '.join(self.answer)


class Wiki:

    def __init__(self, geocode):
        try:
            self.latitude = geocode[0]["geometry"]["location"]["lat"]
            self.longitude = geocode[0]["geometry"]["location"]["lng"]
            self.address = geocode[0]["formatted_address"]
            self.lost = ""
        except IndexError:
            self.latitude = 48.8748465
            self.longitude = 2.3504873
            self.address = 'De retour chez OpenClassrooms... '
            self.lost = """ Désolé mais quand je suis perdu, je reviens
             toujours à mon point de départ! Je ne suis qu'un robot
              après tout..."""
        self.response = {}
        self.some_bargain = ["Ah oui, oui, oui... ",
                             "Bien sur mon petit... ",
                             "Hum, voyons, voyons... ",
                             "Oh, très intéressant oui! ",
                             "Rrrrr... Pardon? Qu'y a-t'il mon poussin? "]
        self.other_blabla = [". Mais sais tu que ... ",
                             """. Voilà ce que
                              je peux te dire ... """,
                             ". Ah je me souviens que ... "]
        wikipedia.set_lang('fr')

    def asking(self):
        self.response["coord"] = {'lat': self.latitude, 'lng': self.longitude}
        if not self.lost:
            self.response["localize"] = wikipedia.geosearch(self.latitude,
                                                            self.longitude)
            self.response["answer"] = choice(self.some_bargain) + self.address
            page = wikipedia.page(title=choice(self.response["localize"]))
            self.response["environment"] = choice(self.other_blabla) + page.summary
            self.response = json.dumps(self.response,
                                       ensure_ascii=False).encode('utf8')
        else:
            self.response["answer"] = self.address
            self.response["environment"] = self.lost
        print(self.response)
        return self.response


class Map:

    def __init__(self, data):
        self.data = data
        self.geo_resp = {}

    def geo_search(self):
        url = "https://maps.googleapis.com/maps/api/geocode/json?"
        parameters = {
            'address': self.data,
            'key': 'AIzaSyD5V82kbhZyYoUJdvuO0E7vUVKY_3AzvOA',
            'language': 'FR',
            'region': 'FR'
        }
        ask = requests.get(url, params=parameters)
        self.geo_resp = ask.json()["results"]
        print(self.geo_resp)
        return self.geo_resp
