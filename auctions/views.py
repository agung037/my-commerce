from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Max
from django.template import RequestContext

from .models import Bid, Categories, Comment, Listing, User, Watchlist
from .forms import CreateListingForm


def index(request):
    listings = Listing.objects.filter(is_active=True)

    # categories
    categories = Categories.objects.all()


    # cari watchlist yang ada pada user
    watchlist_list = []
    if request.user.username:
        watchlist = Watchlist.objects.filter(user = request.user)
        for w in watchlist:
            watchlist_list.append(w.listings)


    return render(request, "auctions/index.html", {
        "listings": listings,
        "wachlist": watchlist_list,
        "categories": categories
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
        

        name = Listing.objects.get(id=request.POST["id_listing"])
        price = float(request.POST["bid"])
        bidder = request.user
        

        if highest_bid is not None and price < highest_bid or price < name.price:
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

            return redirect(f'/listing/{pk}')

    

    listing = Listing.objects.get(id=pk)

    # get the winner
    winner = Bid.objects.filter(listing=listing).first()
    print(winner)

    # get all bid from current listing
    bid = Bid.objects.filter(name=listing)

    # cek apakah listing tersebut ada di dalam watchlist
    watchlist = False
    if request.user.username:
        if Watchlist.objects.filter(listings=listing, user=request.user).exists():
            watchlist = True

    # get all comments in current listing
    comments = Comment.objects.filter(listing=pk)

    return render(request, "auctions/listing.html", {
        "pk":pk,
        "listing": listing,
        "watchlist": watchlist,
        "bid": bid,
        "comments": comments,
        "winner": winner

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

def watchlist(request):
    listings = Listing.objects.all()
    
    # cari watchlist yang ada pada user
    watchlist_list = []
    if request.user.username:
        watchlist = Watchlist.objects.filter(user = request.user)
        for w in watchlist:
            watchlist_list.append(w.listings)

    return render(request, "auctions/watchlist.html", {
        "listings": listings,
        "wachlist": watchlist_list
    })




def watchlist_edit(request, pk):
    if request.method == "POST":
        instruction = request.POST["instruction"]
        listing = Listing.objects.get(id=pk)

        # add into db
        if instruction == "add":
            w = Watchlist(user = request.user, listings = listing)
            w.save()
            print("added")
        else:
            w = Watchlist.objects.get(user = request.user, listings=listing)
            w.delete()
            print("deleted")

    return redirect(f'/listing/{pk}')


def category(request, pk):

    listings = Listing.objects.filter(categories=pk)
    category_name = Categories.objects.get(id=pk)
    categories = Categories.objects.all()

    # cari watchlist yang ada pada user
    watchlist_list = []
    if request.user.username:
        watchlist = Watchlist.objects.filter(user = request.user)
        for w in watchlist:
            watchlist_list.append(w.listings)


    return render(request, "auctions/category.html", {
        "listings" : listings,
        "category_name" : category_name,
        "categories": categories,
        "wachlist": watchlist_list
    })


def listing_status(request, pk):

    if request.method == "POST":
        if request.POST["instruction"] == "close":
            Listing.objects.filter(id=pk).update(is_active=False)
        else:
            Listing.objects.filter(id=pk).update(is_active=True)

    return redirect(f'/listing/{pk}')
        

def comment(request, pk):

    if request.method == "POST":
        comment = request.POST["comment"]
        listing = Listing.objects.get(id=pk)
        c = Comment(comment=comment, user=request.user, listing=listing)
        c.save()
        return redirect(f'/listing/{pk}')
    
    return redirect(f'/listing/{pk}')