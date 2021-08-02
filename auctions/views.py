from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Max

from .models import Bid, Categories, Listing, User
from .forms import CreateListingForm


def index(request):
    listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
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



def listing(request, pk):

    if request.method == "POST":
        # get the highest bid
        highest_bid = Bid.objects.filter(name=pk).aggregate(Max('price')).get('price__max')
        
        print(f"highest bid {highest_bid}")

        name = Listing.objects.get(id=request.POST["id_listing"])
        price = float(request.POST["bid"])
        bidder = request.user
        

        if highest_bid is not None and price < highest_bid:
            return HttpResponse("Error : price has been updated, your bidder is below current price")
        else:
            b = Bid(name=name, price=price, bidder=bidder)
            b.save()
    
            # update curent price
            # filter name and get the highest
            highest_bid = Bid.objects.filter(name=pk).aggregate(Max('price')).get('price__max')
            bid_instance = Bid.objects.filter(name=pk, price=highest_bid).order_by('created_at').first()
            l = Listing.objects.get(id=pk)
            l.current_price = bid_instance
            l.save()

            # print(latest_bidder)

            return HttpResponseRedirect(reverse("listing", args=(request.POST["id_listing"])))


    listing = Listing.objects.get(id=pk)
    watchlist = request.user.watchlist

    return render(request, "auctions/listing.html", {
        "pk":pk,
        "listing": listing,

    })

@login_required
def create_listing_view(request):

    if request.method == "POST":
        form = CreateListingForm(request.POST)

        if form.is_valid():
            creator = request.user
            categories = form.cleaned_data['categories']
            name = form.cleaned_data['name']
            price = form.cleaned_data['price']
            image = form.cleaned_data['image']
            description = form.cleaned_data['description']

            l = Listing(creator=creator, categories=categories, name=name, price=price, image=image, description=description)
            l.save()
            return HttpResponseRedirect(reverse("index"))

    else:
        form = CreateListingForm()

    return render(request, "auctions/create.html", {
        "categories": Categories.objects.all(),
        "form": form
    })