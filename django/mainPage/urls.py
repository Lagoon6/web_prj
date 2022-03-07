from django.urls import path 
from mainPage import views

app_name = "mainPage" 

urlpatterns = [
    path(''              , views.mainPage, name=app_name),   
]