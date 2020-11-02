from django.urls import path

from . import views

app_name = '_covidStocks'
urlpatterns = [
    path('', views.index, name='index'),
]
