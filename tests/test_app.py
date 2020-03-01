# coding: utf-8

from GrandPyBot.application import app
import requests


def test_index_route():
    with app.test_request_context('/', method='GET'):
        assert request.path == '/'
        assert request.method == 'GET'
