from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render  

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes


import tweepy
from tweepy import OAuthHandler


from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import pickle
import tensorflow as tf
# from tensorflow import Graph, Session



# model_graph = Graph()
# with model_graph.as_default():
#     tf_session = tf.compat.v1.Session()
#     with tf_session.as_default():
#         model= load_model('./models/Sentiment_LSTM_model.h5')

# Keras stuff

global graph

graph = tf.compat.v1.get_default_graph()

model = load_model('./models/Sentiment_LSTM_model.h5')
MAX_SEQUENCE_LENGTH = 300

# Twitter
CONSUMER_KEY= "pJkskqhWwTpZnRZVvTySY9pmU"
CONSUMER_SECRET= "76BmlszKh8ECLKDBWza4qR8EqbbFtlZ53tO5WT3gheQXycbvYL"
ACCESS_TOKEN= "1293842701662580736-aVxneRtLhMjZZv0LXBjOW9wLqeSjO0"
ACCESS_SECRET= "U1tkFCw96XZ1mRQTK2q5uXb2v8sMDy6UoFnvliwwEFxmy"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAABFDkwEAAAAA2Bi13XDXQo0%2BMPugHt0T755cT8U%3D9gi4FNdMTrYZ4yZfeoPSKOs84lfuTs3SekB8TRQf3M8xHgrMqk"

# auth = tweepy.OAuth2BearerHandler(BEARER_TOKEN)
# auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
# auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
# api = tweepy.API(auth, wait_on_rate_limit=True)






client  = tweepy.Client(bearer_token=BEARER_TOKEN, consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token=ACCESS_TOKEN, access_token_secret=ACCESS_SECRET)


# loading tokenizer
with open("tokenizer.pickle", "rb") as handle:
    tokenizer = pickle.load(handle)


def predict(text, include_neutral=True):
    # Tokenize text
    x_test = pad_sequences(tokenizer.texts_to_sequences([text]), maxlen=MAX_SEQUENCE_LENGTH)
    # print(text, x_test)
    # Predict
    # with model_graph.as_default():
    #     with tf_session.as_default():
    # model= load_model('./models/Sentiment_LSTM_model.h5')
    score = model.predict([x_test])[0]
    if score >= 0.4 and score <= 0.6:
        label = "Neutral"
    if score <= 0.4:
        label = "Negative"
    if score >= 0.6:
        label = "Positive"

    return {"label": label, "score": float(score)}


# @app.route("/")
def index(request):
    return HttpResponse("Hello World")




# @app.route("/getsentiment", methods=["GET"])

@api_view(('GET',))
def getsentiment(request, text):
    data = {"success": False}
    # if parameters are found, echo the msg parameter
    if text != None:
        # with model_graph.as_default():
        #     with tf_session.as_default():
        data["predictions"] = predict(text)
        # with graph.as_default():
        #     data["predictions"] = predict(text)
        data["success"] = True
    return JsonResponse(data)


# @app.route("/analyzehashtag", methods=["GET"])

@api_view(('GET',))
def analyzehashtag(request, text):

    positive = 0
    neutral = 0
    negative = 0
    tweets = client.search_recent_tweets(query = f"(#{text}) lang:en", max_results = 100)
    # tweets = client.search_recent_tweets(query = text, max_results = 100)
    for tweet in tweets.data:
        # with graph.as_default():
        prediction = predict(tweet.text)
        if prediction["label"] == "Positive":
            positive += 1
        if prediction["label"] == "Neutral":
            neutral += 1
        if prediction["label"] == "Negative":
            negative += 1

    return JsonResponse({"positive": positive, "neutral": neutral, "negative": negative})

# @app.route("/gettweets", methods=["GET"])


@api_view(('GET',))
def gettweets(request, text):
    tweets = []
    query = text
    tweetvalue = client.search_recent_tweets(query = f"(#{query}) lang:en", max_results = 10)
    # tweetvalue = client.search_recent_tweets(query = query, max_results = 10)
    for tweet in tweetvalue.data:
        temp = {}
        temp["text"] = tweet.text
        # temp["username"] = tweet.user.screen_name 
        # with graph.as_default():
        prediction = predict(tweet.text)
        temp["label"] = prediction["label"]
        temp["score"] = prediction["score"]
        tweets.append(temp)

    # return render(request,"results.html", {"results":tweets})
    return JsonResponse({"results": tweets})
