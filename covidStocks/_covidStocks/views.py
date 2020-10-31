from django.shortcuts import render
from django.http import HttpResponse
from vaderSentiment import SentimentIntensityAnalyzer
import yfm
import twitter
from json import load as jsload
# import pandas as pd

COMPANY_DICT = {
    company_names: ['Johnson&Johnson','Pfizer','Moderna','AstraZeneca PLC',
                    'GlaxoSmithKline','NovaVax','Merck'],
    company_symbols: ['JNJ','PFE','MRNA','AZN','GSK','NVAX','MRK'],
    keyWords: [['Johnson&Johnson','$JNJ','Johnson & Johnson'],
               ['Pfizer','$PFE','PFE'],
               ['Moderna','MRNA','$MRNA'],
               ['AstraZeneca','AZN','Astra Zeneca','$AZN'],
               ['GSK','GlaxoSmithKline','$GSK'],
               ['NovaVax','NVAX','$NVAX'],
               ['Merck','MRK','$MRK']]
}

def index(request):
    return HttpResponse("I am in pain.")

def return_twitter_connection():
    with open('../secrets.json','r') as s:
        secrets = jsload(s)
        return twitter.Api(consumer_key=secrets['consumer_key'],
                      consumer_secret=secrets['consumer_secret'],
                      access_token_key=secrets['access_token'],
                      access_token_secret=secrets['access_token_secret'])



def get_tweets(company,stock,keyWords):
    api = return_twitter_connection()
    return api.GetSearch(term=build_search_string(keyWords),since='2020-01-01')


def build_search_string(keyWords):
## Example '(johnson&johnson OR $JNJ OR ("Johnson & Johnson"))'
    search_string = '("' + keyWords[0]
    for w in keyWords:
        search_string = search_string + '" OR "' + w
    search_string = search_string + ')'
    return search_string
