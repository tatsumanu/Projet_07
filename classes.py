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
        self.latitude = geocode[0]["geometry"]["location"]["lat"]
        self.longitude = geocode[0]["geometry"]["location"]["lng"]
        self.address = geocode[0]["formatted_address"]
        self.response = {}
        self.some_bargain = ["Ah oui, oui, oui... ",
                             """ Bien sur mon petit, voilà ce que
                              je peux te dire sur cet endroit... """,
                             "Hum, voyons, voyons... ",
                             "Oh, très intéressant oui! "]
        self.other_blabla = [". Mais sais tu que ... ",
                             ". Juste à côté, il y a aussi ... ",
                             ". Ah je me souviens que ... "]
        wikipedia.set_lang('fr')

    def asking(self):
        self.response["localize"] = wikipedia.geosearch(self.latitude,
                                                        self.longitude)
        self.response["answer"] = choice(self.some_bargain) + self.address
        page = wikipedia.page(title=choice(self.response["localize"]))
        self.response["environment"] = choice(self.other_blabla) + page.summary
        self.response = json.dumps(self.response,
                                   ensure_ascii=False).encode('utf8')
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
