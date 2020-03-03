# coding: utf-8

from GrandPyBot.application import app, index, not_found, credit
from flask import Flask, request, Response
import pytest


@pytest.fixture
def client():
    return app.test_client()


def test_index_route(client):
    with app.test_request_context('/', method='GET'):
        assert request.path == '/'
        assert request.method == 'GET'
        assert client.get('/').status_code == 200
        response = index()
        assert "GrandPy" in response


def test_ajax_search_route(client):
    response = client.post("/ajax_search", data={'question': 'tour eiffel'})
    assert response.status_code == 200


def test_credit_route(client):
    with app.test_request_context('/credit', method='GET'):
        assert request.path == '/credit'
        assert request.method == 'GET'
        assert client.get('/credit').status_code == 200
        response = credit()
        assert "Credits" in response


def test_404_route(client):
    response = client.get('/page_that_doesnt_exists')
    assert response.status_code == 200
    assert b"Il n'y a rien ici ! On perd la boule GrandPy ?" in response.data
