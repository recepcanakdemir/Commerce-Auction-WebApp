from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import ListingForm,CommentForm,BidForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User,Listing,Category,Bid,Watchlist

#listing detail page
def listing(request, listing_id):
    #listing and category

    listing = Listing.objects.get(pk=listing_id)
    category = Category.objects.all().filter(pk= listing_id)
    if listing.creator == request.user:
        creator_user = request.user    
    else:
        creator_user=None   

    #----------------comment form---------------------------------
    comment_form = CommentForm(request.POST or None)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.listing = listing
        comment.save()
        comment_form = CommentForm()
        return HttpResponseRedirect(listing.get_absolute_url())

    # burada baslangic fiyatina sahip bir bid objesi olusturduk. Her listing sayfasina girildiginde yeniden olusturulmamasi icin bu listinge sahip bidleri olusturan querysetin uzunlugun 0 olmasi lazim diye sart koyduk. Yani hic yeni teklif yoksa bu sart calisacak.
    start_bid = listing.starting_price
    bid_form = BidForm(request.POST or None)
    if len(Bid.objects.all().filter(listing=listing)) is 0:
        start_bid_object = Bid.objects.create(user = request.user, listing=listing, price=start_bid)
        start_bid_object.save()
    

    #-----------------bid form section ----------------------------
    current_bid_amount = len(Bid.objects.all().filter(listing=listing))-1
    if bid_form.is_valid():
        bid = bid_form.save(commit=False)
        if bid.price > Bid.objects.all().filter(listing=listing).last().price:
           bid.user = request.user
           bid.listing = listing
           bid.save()
           bid_form = BidForm()
           messages.success(request,"Your bid is the current bid")
           current_bid_amount+=1
           return HttpResponseRedirect(listing.get_absolute_url())
        else:
           messages.error(request,"Your bid must be greater than current price")
           return HttpResponseRedirect(listing.get_absolute_url())
    listing.starting_price = '{:.2f}'.format(float(Bid.objects.all().filter(listing=listing).last().price))

    #----------------close auction section--------------------------
    winner = None
    
  #  if request.method == "POST" or listing.is_closed:
        #listing.is_closed = True 
        #listing.save()
        #winner = Bid.objects.all().filter(listing=listing).last().user
    
    #---------------- add to watchlist section-----------------------
    
    # new POST section

    if request.method == "POST" or listing.is_closed:
        if  request.POST.get("close_auction") or listing.is_closed:
            listing.is_closed = True 
            listing.save()
            winner = Bid.objects.all().filter(listing=listing).last().user
        if request.POST.get("add_to_watchlist"):
            listing.is_in_watchlist = True
            listing.save()
            listing.watchlist.add(request.user)
        if request.POST.get("remove_from_watchlist"):
            listing.is_in_watchlist = False
            listing.save()
            listing.watchlist.remove(request.user)
    if request.user.is_authenticated:
        length_of_watchlist = len(Listing.objects.all().filter(watchlist = request.user))
    else:
        length_of_watchlist=None
    context = {
        "listing":listing,
        "bid_form":bid_form,
        "category":category, 
        "comment_form":comment_form,
        "creator_user":creator_user,
        "is_closed":listing.is_closed,
        "is_in_watchlist":listing.is_in_watchlist,
        "winner":winner,
        "current_bid_amount":current_bid_amount,
        "length_of_watchlist":length_of_watchlist
    }
    return render(request,"auctions/listing.html",context)




#categories page
def categories(request):
    if request.user.is_authenticated:
        length_of_watchlist = len(Listing.objects.all().filter(watchlist = request.user))
    else:
        length_of_watchlist=None
    categories = Category.objects.all()
    return render(request, "auctions/categories.html",{
        "categories":categories,
        "length_of_watchlist":length_of_watchlist
    })

#watchllist page
def watchlist(request):
    user = request.user
    if user.is_authenticated:
        length_of_watchlist = len(Listing.objects.all().filter(watchlist = request.user))
    else:
        length_of_watchlist=None
    listings = Listing.objects.all().filter(watchlist = user)
    context = {
        "listings":listings,
        "length_of_watchlist": length_of_watchlist
    }
    return render(request,"auctions/watchlist.html",context)

#def index(request):
    #return render(request, "auctions/index.html",{
        #"listings":Listing.objects.all()
    #})

def index(request):
    listings = Listing.objects.all()
    if request.user.is_authenticated:
        length_of_watchlist = len(Listing.objects.all().filter(watchlist = request.user))
    else:
        length_of_watchlist=None
    for listing in listings:
        latest_bid = Bid.objects.filter(listing=listing).last()
        listing.starting_price = '{:.2f}'.format(float(latest_bid.price))
    return render(request, "auctions/index.html", {
        "listings": listings,
        "length_of_watchlist":length_of_watchlist
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
        "form":form,
        "length_of_watchlist":len(Listing.objects.all().filter(watchlist = request.user))
    }
    return render(request,'auctions/create.html',context)

def category(request,category_name):
    listings = Listing.objects.filter(category__name= category_name)
    return render(request, "auctions/index.html",{
        "listings":listings,
        "length_of_watchlist":len(Listing.objects.all().filter(watchlist = request.user))
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
            Watchlist.objects.all().create(user = user)
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
