from django.contrib import admin
from django.urls import path
from . import views
  
urlpatterns = [
   path('', views.index, name ='index'),
   path('gettweets/<str:text>', views.gettweets),
   path('analyzehashtag/<str:text>', views.analyzehashtag),
   path('getsentiment/<str:text>', views.getsentiment),
   # path('getsentiment/<str:text>', views.getsentiment),
]