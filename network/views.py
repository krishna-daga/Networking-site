from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User,Posts
from django.contrib.auth.decorators import login_required
    


def index(request):
    #allposts=Posts.objects.values('post')
    #will give a dictionary sort of result : {'post': ' I am excited to be making this project!'}
    allposts=Posts.objects.all().order_by('-time')
    if (len(allposts)==0):
        msg="no posts available"
        return render(request,"network/index.html",{"msg":msg})
    else:
        #print all posts
        return render(request,"network/index.html",{"posts":allposts})
    
@login_required(login_url='/login')
def newpost(request):
    #if new post
    if request.method == "POST":
        #create object
        newpost=Posts()
        newpost.user=request.user
        newpost.post=request.POST.get('post')
        #save it
        newpost.save()
        return HttpResponseRedirect(reverse(index))
    else:
        return render(request,"network/newpost.html")






    


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")







