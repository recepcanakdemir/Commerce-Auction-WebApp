from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import ListingForm,CommentForm,BidForm
from django.contrib.auth.decorators import login_required

from .models import User,Listing,Bid,Category

#listing detail page
def listing(request, listing_id):
    #listing and category
    listing = Listing.objects.get(pk=listing_id)
    category = Category.objects.all().filter(pk= listing_id)
    #comment form
    comment_form = CommentForm(request.POST or None)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.listing = listing
        comment.save()
        comment_form = CommentForm()
    #bid form
    start_bid = listing.price
    bid_form = BidForm(request.POST or None)
    if bid_form.is_valid():
        price = bid_form.save(commit=False)
        if price.price > start_bid:
            price.user = request.user
            price.listing = listing
            price.save()
            bid_form = BidForm()
            listing.value = Bid.objects.all().filter(pk=listing_id) #fix this 
        else:
            listing.value= start_bid
            #error message the offer must be greater than current price
    context = {
        "listing":listing,
        "bid_form":bid_form,
        "category":category, 
        "comment_form":comment_form
    }
    return render(request,"auctions/listing.html",context)




#categores page
def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html",{
        "categories":categories
    })
def index(request):
    return render(request, "auctions/index.html",{
        "listings":Listing.objects.all()
    })




#creating listing page
@login_required(login_url='login')
def create(request):
    form = ListingForm(request.POST or None)
    if form.is_valid():
        listing = form.save(commit=False)
        listing.creator = request.user
        listing.save()
        return HttpResponseRedirect(listing.get_absolute_url())
    context = {
        'form':form
    }
    return render(request,'auctions/create.html',context)

def category(request,category_name):
    listings = Listing.objects.filter(category__name= category_name)
    return render(request, "auctions/index.html",{
        "listings":listings
    })





#login page
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




#logout page
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))





#register page
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
