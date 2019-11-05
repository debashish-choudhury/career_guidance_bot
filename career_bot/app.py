from flask import Flask, render_template, request, jsonify, Response
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import json
import os, uuid
from datetime import datetime
from pytz import timezone
from nltk.tokenize import word_tokenize


app = Flask(__name__)

english_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")

#trainer = ListTrainer(english_bot)
#text = open("engineering.yml", "r")
#training = text.readlines()

trainer = ListTrainer(english_bot)


#trainer.train('chatterbot.corpus.english')
text_file = open("sample.txt", "r")
text = text_file.readlines()



sample_text = [s.replace('\n','') for s in text]
trainer.train(sample_text)
text_file = open("conversations.yml", "r")
text = text_file.readlines()

training_data = [s.replace('\n', '') for s in text]
trainer.train(training_data)


text_file = open("blocked.txt", "r")
block = text_file.readlines()


blocked = [s.replace('\n', '') for s in block]



@app.route("/")
def home():
    return render_template("index.html")



@app.route("/get")
def get_bot_response():

    userText = request.args.get('msg')
    user_words = word_tokenize(userText)

   
    for word in user_words:
        if word in blocked:
            return str("Please avoid swear words!")
         
    
    return str(english_bot.get_response(userText))
    #return str("Hello")





@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }

    resp = jsonify(message)
    resp.status_code = 404

    return resp


@app.errorhandler(500)
def internalservererror(error=None):
    message = {
        'status': 500,
        'message': 'Unexpected server error or Internal Server Error',
    }
    resp = jsonify(message)
    resp.status_code = 500

    return resp

@app.errorhandler(502)
def gatewaytimeout(error=None):
    message = {
        'status': 502,
        'message': 'Gateway time out error',
    }
    resp = jsonify(message)
    resp.status_code = 502

    return resp


@app.errorhandler(400)
def Badrequest(error=None):
    message = {
        'status': 400,
        'message': 'Bad request',
    }
    resp = jsonify(message)
    resp.status_code = 400

    return resp


if __name__ == "__main__":
    app.run()
