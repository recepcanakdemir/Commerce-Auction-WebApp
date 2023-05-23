from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import ListingForm

from .models import User,Listing,Bid,Category


def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    bid =  listing.price.all().last()
    category = Category.objects.all().filter(pk= listing_id)
    return render(request,"auctions/listing.html",{
        "listing":listing,
        "comments":listing.comment.all(),
        "bid":bid,
        "category":category
    })      

def index(request):
    return render(request, "auctions/index.html",{
        "listings":Listing.objects.all()
    })

def create(request):
    form = ListingForm(request.POST or None)
    if form.is_valid():
        listing = form.save()
        return HttpResponseRedirect(listing.get_absolute_url())
    context = {
        'form':form
    }
    return render(request,'auctions/create.html',context)



def category(request,category_name):
    listing = Category.objects.get(name=category_name).listings.all()
    return render(request,"auctions/index.html", {
        "listings":listing
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
