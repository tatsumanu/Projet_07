# coding: utf-8

from GrandPyBot.classes import Map
import requests

""" Tests for the Map class. Run them with 'pytest' instruction
in command line unit directly at the root of the project """


class MockResponse:

    @staticmethod
    def json():
        return {"results": "map_geosearch_response"}


def test_map_class_init():
    answer_class_response = "Tour Montparnasse"
    coordonates = Map(answer_class_response)
    assert coordonates.data == "Tour Montparnasse"
    assert coordonates.geo_resp == {}


def test_map_geo_search(monkeypatch):

    map_object = Map("Tour Montparnasse")

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    result = map_object.geo_search()
    assert result == "map_geosearch_response"
