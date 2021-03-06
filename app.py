
import os
import math
from flask import Flask
from flask import render_template, request, jsonify
import json


import politeness
from politeness.classifier import Classifier
from politeness.helpers import set_corenlp_url
import politeness.strategies as ps
set_corenlp_url('http://localhost:9000')

cls = Classifier()

app = Flask(__name__)
# app.config.from_object(os.environ['APP_SETTINGS'])


# @app.route("/")
# def hello():
#     return "Hello world, it's the Politeness Classifier!"


@app.route("/")
def text_input_form():
    return render_template("politeness-form.html")


# @app.route("/")
# def text_input_form2():
#     return render_template("politeness-form.html")


@app.route("/score-politeness", methods=['POST'])
def score_text():
    text = request.form['text']
    probs = cls.predict(text)

    # Based on probs, determine label and confidence
    # print(probs)
    # if probs['polite'] > 0.6:
    #     l = "polite"
    #     confidence = probs['polite']
    # elif probs['impolite'] > 0.6:
    #     l = "impolite"
    #     confidence = probs['impolite']
    # else:
    #     l = "neutral"
    #     confidence = 1.0 - math.fabs(probs['polite'] - 0.5)
    #
    # confidence = "%.2f" % confidence

    #new attempt at code
    endIndex = len(probs) - 1
    print(text)
    predictionSeg = probs[endIndex]
    # print(predictionSeg)
    doc = predictionSeg["document"]
    parses = predictionSeg["parses"]

    stratDict = (ps.sentCheck(text)) #creates dictionary based on helper in strategies.py

    fullParse = parses[0]
    parsing = fullParse["parses"] #stores parsing information from nltk

    formattedParse = str(parsing)
    formattedParse = formattedParse.replace("),", ") , ") #stores parsing and then makes the string less cluttered


    politeProb = float(doc[0]) #probability of sentiment being polite
    impoliteProb = float(doc[1]) #inverse
    # print(politeProb)
    # print(impoliteProb)

    if politeProb > 0.6: #math and conditions preserved from previous
        l = "polite"
        confidence = politeProb
    elif impoliteProb > 0.6:
        l = "impolite"
        confidence = impoliteProb
    else:
        l = "neutral"
        confidence = 1.0 - math.fabs(politeProb - .5)

    confidence = "%.2f" % confidence

    # Return JSON:
    return jsonify(text=text, label=l, confidence=confidence, parsing=formattedParse, strategies=json.dumps(stratDict), stratObj=stratDict)
    #strategies returns the string version of the strategy dictionary, while stratObj returns the Python dictionary (not useful for printing)

if __name__ == "__main__":
    # port = int(os.environ.get("PORT", 8000))
    # app.run(host='0.0.0.0', port=port)
    set_corenlp_url('localhost:9000')
    app.run()
