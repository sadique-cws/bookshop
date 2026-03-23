from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


# admin panel and user login and resgistration view


def login(req):
    # check if already logged in
    if req.user.is_authenticated:
        return redirect("homepage")
    
    
    form = LoginForm(req.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        login_user = authenticate(username=username, password=password)
        if login_user is not None:
            auth_login(req, login_user)
            return redirect("homepage")
        
        form.add_error(None, "Invalid username or password")

    return render(req, "auth/login.html", {"form": form})


def register(req):
    form = RegisterForm(req.POST or None)
    if form.is_valid():
        password = form.cleaned_data.get("password")
        
        # encrypt password and save user to database
        data = form.save(commit=False)
        data.set_password(password)
        data.save()
        return redirect("login")
    return render(req,"auth/register.html", {"form": form}) 


def logout(req):
    auth_logout(req)
    return redirect("login")
