from django.shortcuts import render
from django.http import HttpResponse
# from vaderSentiment import SentimentIntensityAnalyzer
from . import models
import yfm
# import pandas as pd
from . import twitter_scrapper as ts

def index(request):
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
    # ts.get_tweets(keyWords=COMPANY_DICT['keyWords'][1])
    return HttpResponse()
