from django.shortcuts import render

def login(request):
    return render(request, "login.html",
    
    )

def mainPage(request):
    return render(request, "mainPage.html",
    
    )