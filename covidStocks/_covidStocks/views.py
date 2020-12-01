from django.shortcuts import render
from django.views.generic.list import ListView
from django.http import HttpResponse
from django.db.models import Q
import pprint
from .forms import TweetForm,TweetEdit
import pandas as pd

from . import models
import yfm
from django.db.models import Avg, Count
from . import twitter_scrapper as ts
from . import stocks
import logging
from django_pandas.io import read_frame

logger = logging.getLogger(__name__)


def index(request):
    if request.method == "POST":
        form = TweetForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return show(request)
            except:
                logger.error("OOF")
                pass
    # try:
    #     models.Company.objects.all().delete()
    #     # models.Tweets.objects.all().delete()
    # except Exception:
    #     pass

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
    stockFetcher = yfm.fetcher()
    stockFetcher.update()

    # for name,sym in zip(COMPANY_DICT['company_names'],COMPANY_DICT['company_symbols']):
    #     models.Company.objects.create(Name = name,symbol=sym)



    tweets = ts.get_tweets(dict=COMPANY_DICT)

    for t in tweets:
        compID = models.Company.objects.get(Name=t.company)
        try:
            models.Tweets.objects.get(tweetID=t.id)
        except:
            models.Tweets.objects.create(tweetID=t.id,
                                     companyID=compID,
                                     date=t.timestamp,
                                     text=t.text,
                                     userID=t.userID,
                                     score=t.score,
                                     interactions=t.interactions)
    # models.Tweets.full_clean()
    # models.Tweets.save()
    sentiment = models.Tweets.objects.values(
                                            'date','companyID__symbol'
                                            ).annotate(
                                                Sentiment = Avg('score')
                                                      )

    sentiment = read_frame(sentiment).pivot(index="date",
                                            columns="companyID__symbol",
                                            values="Sentiment").fillna(value=0,axis=1)
    sentiment.index = pd.to_datetime(sentiment.index)
    stocks.write_predictions(COMPANY_DICT['company_symbols'],sentiment)
    form = TweetForm()
    return render(request,'index.html',{'form':form})


def show(request):
    tweets = models.Tweets.objects.all()
    return render(request,"show.html",{'tweetsArr':tweets})
class show2(ListView):
    model = models.Tweets
    paginate_by=25

    def get_queryset(self):
        tweets = models.Tweets.objects.all()
        query = self.request.GET.get("q")
        if query:
            tweets = models.Tweets.objects.filter(
                Q(text__icontains=query)
            )
        return tweets
def edit(request, id):
    tweets = models.Tweets.objects.get(tweetID=id)
    return render(request,'edit.html', {'tweet':tweets})

def update(request, id):
    tweets = models.Tweets.objects.get(tweetID=id)
    form = TweetForm(request.POST, instance = tweets)

    if form.is_valid():
        form.save()
        return show(request)
    else: logger.error(form.errors)
    return render(request, 'edit.html', {'tweet': tweets})

def destroy(request, id):
    tweets = models.Tweets.objects.get(tweetID=id)
    tweets.delete()
    return show(request)
