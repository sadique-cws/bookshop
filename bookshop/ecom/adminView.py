from django.shortcuts import redirect, render
from ecom.models import *
from ecom.forms import * 

def dashboard(req):
    return render(req, "admin/dashboard.html") 


def manageGenere(req):
    data = {}
    form = GenereForm(req.POST or None)
    data["generes"] = Genere.objects.all()
    data["form"] = form

    if req.method == "POST":
        if form.is_valid():
            data = form.save(commit=False)
            data.slug = data.title.lower().replace(" ", "-")
            data.save()
            return redirect("admin_manage_genere")
    return render(req, "admin/manage_genere.html", data)

def insertBook(req):
    data = {}
    form = BookForm(req.POST or None, req.FILES or None)
    data["form"] = form

    if req.method == "POST":
        if form.is_valid():
            data = form.save(commit=False)
            data.slug = data.title.lower().replace(" ", "-")
            data.save()
            return redirect("admin_manage_book")
    return render(req, "admin/insert_book.html",data)


def manageBooks(req):
    data = {}
    data["books"] = Book.objects.all()
    return render(req,"admin/manage_book.html",data)

def manageAuthor(req):
    data = {}
    form = AuthorForm(req.POST or None)
    data["authors"] = Author.objects.all()
    data["form"] = form

    if req.method == "POST":
        if form.is_valid():
            data = form.save(commit=False)
            data.slug = data.name.lower().replace(" ", "-")
            data.save()
            return redirect("admin_manage_author")
    return render(req, "admin/manage_author.html",data)