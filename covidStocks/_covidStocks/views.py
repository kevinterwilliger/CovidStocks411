from django.shortcuts import render
from django.http import HttpResponse
# from vaderSentiment import SentimentIntensityAnalyzer
from . import models
import yfm
# import pandas as pd
from . import twitter_scrapper as ts

def index(request):
    try:
        models.Company.objects.all().delete()
        models.Tweets.objects.all().delete()
    except Exception:
        pass
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
    for name,sym in zip(COMPANY_DICT['company_names'],COMPANY_DICT['company_symbols']):
        models.Company.objects.create(Name = name,symbol=sym)

    tweets = ts.get_tweets(dict=COMPANY_DICT)

    for t in tweets:
        compID = models.Company.objects.get(Name=t.company)
        models.Tweets.objects.create(companyID=compID,
                                     date=t.timestamp,
                                     text=t.text,
                                     userID=t.userID,
                                     score=t.score,
                                     interactions=t.interactions)

    return HttpResponse("hi")
