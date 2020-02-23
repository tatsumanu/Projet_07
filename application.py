# coding: utf-8

# making necessary imports
from flask import Flask, render_template, request
from classes import Answer, Wiki, Map

app = Flask(__name__)


# base url
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index_2.html")


# url called when submitting a query
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


# 404 error page
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(debug=True)
