# coding: utf-8

from GrandPyBot.classes import Answer
import json
import pytest

""" Tests for the Answer class. Run them with 'pytest' instruction
in command line unit directly at the root of the project """

question = "Pourrais-tu me donner l'adresse de la Tour Eiffel s'il te\
 plait!"


@pytest.fixture
def answer():
    return Answer(question)


def test_answer_class(answer):
    assert answer.question == question
    assert answer.answer == []
    assert answer.answer != "Pourrais-tu me donner l'adresse de la Tour Eiffel\
   s'il te plait!"


def test_searching_method_from_answer_class(answer):
    assert answer.searching() == "Pourrais tu me l adresse de la Tour Eiffel\
 s il te plait"
    assert answer.answer != []
