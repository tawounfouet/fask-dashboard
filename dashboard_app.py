# _*_ coding: utf-8 _*_
from flask import Flask
from flask import render_template, request, url_for, jsonify
import json
import requests

app = Flask(__name__)

#https://home.openweathermap.org/api_keys
METEO_API_KEY = "c5d42843a49dc27e2ffc86a57d8dc44a"


if METEO_API_KEY is None:
    #URL de test:
    METEO_API_URL = "https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx"
else:
    # URL avec clé
    METEO_API_URL =  "https://api.openweathermap.org/data/2.5/forecast?lat=48.883587&lon=2.333779&appid=" + METEO_API_KEY

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/dashboard/")
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/meteo_test/')
def meteo_test():
    dictionnaire = {
        "type": "Prévision de température",
        "valeurs": [24, 24, 25, 26, 27, 28],
        "unite": "dégrés Celcius"
    }
    return jsonify(dictionnaire)

@app.route('/api/meteo/')
def meteo():
    response = requests.get(METEO_API_URL)
    content = json.loads(response.content.decode('utf-8'))

    if response.status_code != 200:
        return jsonify({
            'status': 'error',
            'message': 'La requête à l\'API météo n\'a pas fonctionné. Voici le message renvoyé par    l\'API : {}'.format(content['message'])
        }), 500

    data = []

    for prev in content["list"]:
        datetime = prev['dt'] * 1000 # conversion du timestamp en millisecondes
        temperature = prev["main"]["temp"] - 273.15 # conversion de Kelvin en °C
        temperature = round(temperature, 2)
        data.append([datetime, temperature])


    return jsonify({
        'status': 'ok',
        'data': data
    })




from functions import extract_keywords


NEWS_API_KEY = "3b002a28871b4497ab818d2139d81cb4" # Remplacez None par votre clé NEWSAPI, par exemple "4116306b167e49x993017f089862d4xx"

if NEWS_API_KEY is None:
    # URL de test :
    NEWS_API_URL = "https://s3-eu-west-1.amazonaws.com/course.oc-static.com/courses/4525361/top-headlines.json" # exemple de JSON
else:
    # URL avec clé :
    NEWS_API_URL = "https://newsapi.org/v2/top-headlines?sortBy=publishedAt&pageSize=100&language=fr&apiKey=" + NEWS_API_KEY


# kw_extractor = yake.KeywordExtractor(top=100, stopwords=None)
# #keywords = kw_extractor.extract_keywords(full_text)
# for kw, v in keywords:
#   print("Keyphrase: ",kw, ": score", v)


@app.route('/api/news/')
def get_news():
 
    response = requests.get(NEWS_API_URL)
    content = json.loads(response.content.decode('utf-8'))

    if response.status_code != 200:
        return jsonify({
            'status': 'error',
            'message': 'La requête à l\'API des articles d\'actualité n\'a pas fonctionné. Voici le message renvoyé par l\'API : {}'.format(content['message'])
        }), 500

    keywords, articles = extract_keywords(content["articles"])



    return jsonify({
        'status'   : 'ok',
        'data'     :{
            'keywords' : keywords[:100], # On retourne uniquement les 100 premiers mots
            'articles' : articles
        }
    })




# if __name__ == "__main__":
#     app.run(debug=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5501, debug=True)