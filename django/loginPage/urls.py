from django.urls import path 
from loginPage import views

app_name = "loginPage" 

urlpatterns = [
    path(''              , views.loginPage, name=app_name), 
    path('get_post', views.get_post, name='get_post'),    
]