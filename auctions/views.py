from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .forms import ListingForm,CommentForm,BidForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User,Listing,Category,Bid

#listing detail page
def listing(request, listing_id):
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
           messages.success(request,"Your bid is the current bid!")
           current_bid_amount+=1
           return HttpResponseRedirect(listing.get_absolute_url())
        else:
           messages.error(request,"Your bid must be greater than current price")
           return HttpResponseRedirect(listing.get_absolute_url())
    listing.starting_price = '{:.2f}'.format(float(Bid.objects.all().filter(listing=listing).last().price))
    if request.user.is_authenticated:
        length_of_watchlist= len(Listing.objects.filter(user_watchlist=request.user))
    else:
        length_of_watchlist=0
    #----------------close auction section--------------------------
    winner = None   
    context = {
        "listing":listing,
        "bid_form":bid_form,
        "category":category, 
        "comment_form":comment_form,
        "creator_user":creator_user,
        "is_closed":listing.is_closed,
        "winner":winner,
        "current_bid_amount":current_bid_amount,
        "is_in_watchlist": listing.user_watchlist.filter(id = request.user.id).exists(),
        "length_of_watchlist":length_of_watchlist
    }
    return render(request,"auctions/listing.html",context)

#add to watchlist or remove from watchlist
@login_required
def add_to_watchlist(request, listing_id):
    listing = get_object_or_404(Listing,id=listing_id)
    if listing.user_watchlist.filter(id = request.user.id).exists():
        listing.user_watchlist.remove(request.user)
        messages.success(request, "Removed  '" + listing.name + "' from your watchlist")
    else:
        listing.user_watchlist.add(request.user)
        messages.success(request, "Added  '" + listing.name + "' to your watchlist")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])



#watchlist page
@login_required
def watchlist(request):
    listings = Listing.objects.filter(user_watchlist=request.user)
    if request.user.is_authenticated:
        length_of_watchlist= len(Listing.objects.filter(user_watchlist=request.user))
    else:
        length_of_watchlist=0
    return render(request,"auctions/watchlist.html",{
        "listings":listings,
        "length_of_watchlist":length_of_watchlist
    })



#categories page
def categories(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        length_of_watchlist= len(Listing.objects.filter(user_watchlist=request.user))
    else:
        length_of_watchlist=0
    return render(request, "auctions/categories.html",{
        "categories":categories,
        "length_of_watchlist":length_of_watchlist
    })



#main listings page
def index(request):
    listings = Listing.objects.all()
    if request.user.is_authenticated:
        length_of_watchlist= len(Listing.objects.filter(user_watchlist=request.user))
    else:
        length_of_watchlist=0
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
    if request.user.is_authenticated:
        length_of_watchlist= len(Listing.objects.filter(user_watchlist=request.user))
    else:
        length_of_watchlist=0
    form = ListingForm(request.POST or None)
    if form.is_valid():
        listing = form.save(commit=False)
        listing.creator = request.user
        listing.save()
        return HttpResponseRedirect(listing.get_absolute_url())
    context = {
        "form":form,
        "length_of_watchlist":length_of_watchlist
    }
    return render(request,'auctions/create.html',context)



#categories page
def category(request,category_name):
    if request.user.is_authenticated:
        length_of_watchlist= len(Listing.objects.filter(user_watchlist=request.user))
    else:
        length_of_watchlist=0
    listings = Listing.objects.filter(category__name= category_name)
    return render(request, "auctions/index.html",{
        "listings":listings,
        "length_of_watchlist":length_of_watchlist
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
