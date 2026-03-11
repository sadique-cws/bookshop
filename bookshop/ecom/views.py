from django.shortcuts import render
from .models import *

# Create your views here.

def homepage(req):
    data = {
        "title":"Home",
        "generes":Genere.objects.all(),
        "books":Book.objects.all()
    }
    return render(req, "home.html", data) 

def filter(req):
    pass 

def book_view(req, slug):
    pass 