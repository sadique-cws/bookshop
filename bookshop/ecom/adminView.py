from django.shortcuts import redirect, render
from ecom.models import *
def dashboard(req):
    return render(req, "admin/dashboard.html") 


def manageGenere(req):
    data = {}
    data["generes"] = Genere.objects.all()
    return render(req, "admin/manage_genere.html", data)


def manageBooks(req):
    data = {}
    data["books"] = Book.objects.all()
    return render(req,"admin/manage_book.html",data)

def manageAuthor(req):
    data = {}
    data["authors"] = Author.objects.all()
    return render(req, "admin/manage_author.html",data)