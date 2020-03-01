# coding: utf-8

from GrandPyBot.classes import Wiki
import wikipedia

""" Tests for the Wiki class. Run them with 'pytest' instruction
in command line unit directly at the root of the project """

FAKE_API_RESULT = {
    'localize': ['OpenClassrooms'],
    'environment': "7 rue Paradis, Paris",
    'coord': {'lat': 'latitude', 'lng': 'longitude'},
    'answer': 'returned_address'
    }

data = [
        {'formatted_address': 'returned_address',
         'geometry': {'location': {'lat': 'latitude', 'lng': 'longitude'}}
         }
     ]

wiki = Wiki(data)


def test_wiki_class_init():
    # basic case
    assert wiki.latitude == "latitude"
    assert wiki.longitude == "longitude"
    assert wiki.address == "returned_address"
    assert wiki.lost == ""


def test_wiki_class_no_response_from_map():
    # No response from map API request
    if data == []:
        assert wiki.lost == """ Désolé mais quand je suis perdu, je reviens
         toujours à mon point de départ! Je ne suis qu'un robot
          après tout..."""
        assert wiki.address == 'De retour chez OpenClassrooms... '


def test_wiki_class_asking(monkeypatch):

    class MockResponse(list):
        def __init__(self, *args):
            list.__init__(self, ["OpenClassrooms"])

        def __len__(self):
            return 1

        def geosearch(self, *args):
            return []

    def mock_page(title=None):

        class Summary:
            def __init__(self):
                self.summary = "7 rue Paradis, Paris"

        result = Summary()
        return result

    monkeypatch.setattr(wikipedia, "geosearch", MockResponse)
    monkeypatch.setattr(wikipedia, "page", mock_page)

    assert wiki.asking()['localize'] == FAKE_API_RESULT['localize']
    assert wiki.asking()['coord'] == FAKE_API_RESULT['coord']
    assert FAKE_API_RESULT['answer'] in wiki.asking()['answer']
    assert FAKE_API_RESULT['environment'] in wiki.asking()['environment']
