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

def filter(req, slug=None):
    if slug is None:
        search_query = req.GET.get("search", "")
        data = {
            "generes":Genere.objects.all(),
            "books":Book.objects.filter(title__icontains=search_query),
            "title": search_query
        }
        return render(req, "filter.html", data)
    else:
        data = {
            "generes":Genere.objects.all(),
            "books":Book.objects.filter(genere__slug=slug),
            "title":Genere.objects.get(slug=slug).title
        }
        return render(req, "filter.html", data)

def book_view(req, slug):
    pass 