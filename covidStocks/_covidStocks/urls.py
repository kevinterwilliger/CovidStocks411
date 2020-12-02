from django.urls import path

from . import views

app_name = '_covidStocks'
urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('create', views.create, name='create'),
    path('show',views.show,name='show'),
    path('show2',views.show2,name='show2'),
    path('edit/<int:id>',views.edit,name='edit'),
    path('delete/<int:id>',views.destroy,name='delete'),
    path('update/<int:id>', views.update,name='update'),
]
