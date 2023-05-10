from django.contrib import admin
from django.urls import path
from . import views
  
urlpatterns = [
   path('', views.index, name ='index'),
   path('gettweets/', views.gettweets),
   path('analyzehashtag/', views.analyzehashtag),
   path('getsentiment/', views.getsentiment),
   # path('getsentiment/', views.getsentiment),
]
