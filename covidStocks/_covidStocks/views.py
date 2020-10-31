from django.shortcuts import render
from django.http import HttpResponse
from vaderSentiment import SentimentIntensityAnalyzer
import yfm

def index(request):
    return HttpResponse("I am in pain.")
