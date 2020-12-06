from django.shortcuts import render
from django.conf import settings
from django.views.generic.list import ListView
from django.http import HttpResponse
from django.db.models import Q
import pprint
from .forms import TweetForm,TweetEdit
import pandas as pd
from django.template.loader import render_to_string
from django.http import JsonResponse
from . import models
import yfm
from django.db.models import Avg, Count
from . import twitter_scrapper as ts
from . import stocks
import logging
from django_pandas.io import read_frame
from django.contrib.staticfiles import finders



logger = logging.getLogger(__name__)

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
    sentiment = models.Tweets.objects.values(
                                            'date','companyID__symbol'
                                            ).annotate(
                                                Sentiment = Avg('score')
                                                      )

    sentiment = read_frame(sentiment).pivot(index="date",
                                            columns="companyID__symbol",
                                            values="Sentiment").fillna(value=0,axis=1)
    sentiment.index = pd.to_datetime(sentiment.index)
    # stocks.write_predictions(COMPANY_DICT['company_symbols'],sentiment)
    return render(request,'index.html')


def create(request):
    if request.method == "POST":
        form = TweetForm(request.POST)
        if form.is_valid():
            try:
                logger.error("here")
                form.save()
                return show(request)
            except:
                logger.error("OOF")
                pass
    form = TweetForm()
    logger.error("bruh")
    return render(request,'create.html',{'form':form})


def show(request):
    ctx = {}
    url_parameter = request.GET.get("q")

    if url_parameter:
        print('yes params')
        tweets = models.Tweets.objects.filter(text__icontains=url_parameter)
    else:
        print("no params")
        tweets = models.Tweets.objects.all()

    ctx["tweetsArr"] = tweets


    if request.is_ajax():
        print('is ajax')
        html = render_to_string(
            template_name="tweets-results-partial.html",
            context=ctx
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    return render(request, "show.html", context=ctx)

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
