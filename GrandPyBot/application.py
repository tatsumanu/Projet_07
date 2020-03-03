# coding: utf-8

# making necessary imports
from flask import Flask, render_template, request
from .classes import Answer, Wiki, Map

app = Flask(__name__)

app.config.from_object('config')


# base url
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# url called when the user submits a question for GrandPy
@app.route("/ajax_search", methods=["POST"])
def search():
    question = request.form['question']
    answer = Answer(question)
    reponse = answer.searching()
    print(reponse)
    gmap = Map(reponse)
    geocode = gmap.geo_search()
    wiki = Wiki(geocode)
    response = wiki.asking()
    return response


# credits page
@app.route("/credit", methods=["GET"])
def credit():
    return render_template("credits.html")


# 404 error page
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run()
