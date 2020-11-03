import twitter
from json import load as jsload
# import pandas as pd
import textblob as tb
from datetime import datetime
# import math

COMPANY_DICT = {
    'company_names': ['Johnson&Johnson','Pfizer','Moderna','AstraZeneca PLC',
                    'GlaxoSmithKline','NovaVax','Merck'],
    'company_symbols': ['JNJ','PFE','MRNA','AZN','GSK','NVAX','MRK'],
    'keyWords': [['Johnson&amp;Johnson','$JNJ','Johnson &amp; Johnson',"-Johnson"],
               ['Pfizer','$PFE','PFE'],
               ['Moderna','MRNA','$MRNA'],
               ['AstraZeneca','AZN','Astra Zeneca','$AZN'],
               ['GSK','GlaxoSmithKline','$GSK'],
               ['NovaVax','NVAX','$NVAX'],
               ['Merck','MRK','$MRK']]
}

class Tweet():
    def __init__(self, t, company):
        self.timestamp = datetime.strptime(t.created_at,"%a %b %d %H:%M:%S %z %Y")
        self.text = t.text
        self.userID = t.user.id
        self.score = tb.TextBlob(t.text).sentiment.polarity
        self.interactions = t.retweet_count + t.favorite_count
        self.company = company

def return_twitter_connection():
    with open('secrets.json','r') as s:
        secrets = jsload(s)
        return twitter.Api(consumer_key=secrets['consumer_key'],
                      consumer_secret=secrets['consumer_secret'],
                      access_token_key=secrets['access_token'],
                      access_token_secret=secrets['access_token_secret'])

def get_tweets(dict):
    api = return_twitter_connection()
    ret = {}
    for comp,keys in zip(dict['company_names'],dict['keyWords']):
        ret[comp] = api.GetSearch(term=build_search_string(keys),since='2020-01-01',count=100)
    return clean_tweets(ret)

## Twitter api requires a search string in a particular manner
# Something like:
# (johnson&johnson OR j&j OR JNJ OR $JNJ) -Johnson lang:en
def build_search_string(keyWords):
    search_string = '("' + keyWords[0]
    minus_word = ""
    for w in keyWords:
        if w[0] == "-":
            minus_word = w
        search_string = search_string + '" OR "' + w
    search_string = search_string + ') lang:en '
    if minus_word != "":
        search_string = search_string + " " + minus_word
    return search_string

def clean_tweets(tweets):
    ret = []
    for comp in tweets:
        for t in tweets[comp]:
            ins = Tweet(t,comp)
            ret.append(ins)
    return ret
