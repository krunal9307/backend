
import tweepy
from tweepy import OAuthHandler

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import pickle
from tensorflow.compat.v1 import get_default_graph
import tensorflow as tf


global graph

graph = get_default_graph()

MAX_SEQUENCE_LENGTH = 300
model = load_model("C:/Users/Saurabh/Desktop/twitter_sentimental_analysis/server/Sentiment_CNN_model.h5")


# loading tokenizer
with open("C:/Users/Saurabh/Desktop/twitter_sentimental_analysis/server/tokenizer.pickle", "rb") as handle:
    tokenizer = pickle.load(handle)


def predict(text, include_neutral=True):
    # Tokenize text
    x_test = pad_sequences(tokenizer.texts_to_sequences([text]), maxlen=MAX_SEQUENCE_LENGTH)

    # Predict
    score = model.predict([x_test])[0]
    if score >= 0.4 and score <= 0.6:
        label = "Neutral"
    if score <= 0.4:
        label = "Negative"
    if score >= 0.6:
        label = "Positive"
    
    print(label, score)
    # return {"label": label, "score": float(score)}

def analyzehashtag(text):

    positive = 0
    neutral = 0
    negative = 0
    # tweets = client.search_recent_tweets(query = text, max_results = 100)
    # for tweet in tweets.data:
    with graph.as_default():
        prediction = predict(text)
    if prediction["label"] == "Positive":
        positive += 1
    if prediction["label"] == "Neutral":
        neutral += 1
    if prediction["label"] == "Negative":
        negative += 1

    print(positive, negative, neutral)

analyzehashtag(text = "God is good")
