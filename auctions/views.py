from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
# Login ftn
from django.contrib.auth.decorators import login_required
# Import all Models from db
from .models import User, Listing, Category, Bid, Comment, WatchList
# form for Create a List
from .forms import CreateListingForm, CreateCatgoryForm

# ================================================
#               index  Function
# ================================================


def index(request):

    return render(request, "auctions/index.html",
                  # Display all items in Model Listing , exclude sold items
                  {"all_listings": Listing.objects.filter(sold=False)
                   })

# ================================================
#               login Function
# ================================================


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

# ================================================
#               logout Function
# ================================================


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# ================================================
#               register Function
#              Built-in User class
# ================================================


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

# ================================================
#              listing  Function
# ================================================

# create a listing


@login_required
def CreateListing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            bid = form.cleaned_data["bid"]
            image_url = form.cleaned_data["image_url"]
            user = request.user
            category_id = Category.objects.get(id=request.POST["categories"])
            Listing.objects.create(user=user, title=title, description=description,
                                   price=bid, image_url=image_url, category=category_id)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "auctions/create.html", {
            "create_listing_form": CreateListingForm(),
            # Show all the catgories when creating a lisitng
            "categories": Category.objects.all()
        })

# Linking Up the databases


@login_required
def DB_Detail_Ref(request, listing_id):
    # Get info from Lisitng DB (Model)
    listing = Listing.objects.get(id=listing_id)
    # Get users
    user = request.user
    # check user is the item's owner
    is_owner = True if listing.user == user else False
    # Get info from Catgory DB (Model)
    category = Category.objects.get(category=listing.category)
    # Get info from Comment DB (Model)
    comments = Comment.objects.filter(listing=listing.id)
    # Get info from WatchList DB (Model)
    watching = WatchList.objects.filter(user=user, listing=listing)
    if watching:
        watching = WatchList.objects.get(user=user, listing=listing)
    return listing, user, is_owner, category, comments, watching

# Listing in list_detail page
# Create Comment for each listing


@login_required
def listing(request, listing_id):
    # * Get details from Listing DB function
    info = DB_Detail_Ref(request, listing_id)
    # ! Get necessary info from DB_Detail_Ref function just for Listing ONLY
    listing, user, is_owner, category = info[0], info[1], info[2], info[3]

# if method is === POST
    if request.method == "POST":
        comment = request.POST["comment"]
        if comment != "":
            # * Create Comments for eech Posts
            Comment.objects.create(user=user, listing=listing, comment=comment)

    return render(request, "auctions/list_details.html", {
        # ! Use same name for all the Key values.
        # lisitng: Show all listing ,
        "listing": listing,
        # catgory: item's catgory,
        "category": category,
        # comments: item's comments , for loop
        "comments": Comment.objects.filter(listing=listing.id),
        # item be watched ?
        "watching": WatchList.objects.filter(user=user, listing=listing).values('watching'),
        # Is the owner are currently login ?
        "is_owner": is_owner
    })

# ================================================
#               watchlist Function
# ================================================


@login_required
def watchlist(request, user_id):
    # filter by id and user
    listing_ids = WatchList.objects.filter(user=request.user, watching=True).values('listing')
    listing = Listing.objects.filter(id__in=listing_ids)
    # list items be watched
    return render(request, "auctions/watchlist.html", {
        "listings": listing
    })


# add_watchlist Function
@login_required
def add_watchlist(request, listing_id):
    # Get details from Listing DB function
    # ! Get necessary info from DB_Detail_Ref function just for Listing ONLY
    info = DB_Detail_Ref(request, listing_id)
    listing, user, is_owner, category, comments = info[0], info[1], info[2], info[3], info[4]
    # filter by user and listing_id
    watch = WatchList.objects.filter(user=user, listing=listing)
    if watch:
        watch = WatchList.objects.get(user=user, listing=listing)
        # Change the status of watchlist in DB
        # and then save the latest status to DB
        watch.watching = True
        watch.save()
    else:
        WatchList.objects.create(user=user, listing=listing, watching=True)

    return render(request, "auctions/list_details.html", {
        # ! Use same name for all the Key values.
        # lisitng: Show all listing ,
        "listing": listing,
        # catgory: item's catgory,
        "category": category,
        # comments: item's comments , for loop
        "comments": comments,
        # item be watched ?
        "watching": WatchList.objects.get(user=user, listing=listing).watching,
        # Is the owner are currently login ?
        "is_owner": is_owner
    })
# remove_watchlist Function


@login_required
def remove_watchlist(request, listing_id):
    # Get details from Listing DB function
    # ! Get necessary info from DB_Detail_Ref function just for Listing ONLY
    info = DB_Detail_Ref(request, listing_id)
    listing, user, is_owner, category, comments, watch = info[0], info[1], info[2], info[3], info[4], info[5]
    # Change the status of watchlist in DB
    # and then save the latest status to DB
    watch.watching = False
    watch.save()

    return render(request, "auctions/list_details.html", {
        # ! Use same name for all the Key values.
        # lisitng: Show all listing ,
        "listing": listing,
        # catgory: item's catgory,
        "category": category,
        # comments: item's comments , for loop
        "comments": comments,
        # item be watched ?
        "watching": WatchList.objects.get(user=user, listing=listing).watching,
        # Is the owner are currently login ?
        "is_owner": is_owner
    })
# ================================================
#               bidding Function
# ================================================


@login_required
def bidding(request, listing_id):
    # Get details from Listing DB function
    # ! Get necessary info from DB_Detail_Ref function just for Listing ONLY
    info = DB_Detail_Ref(request, listing_id)
    listing, user, is_owner, category, comments, watch = info[0], info[1], info[2], info[3], info[4], info[5]
    if request.method == "POST":
        # post a Bid
        bid = request.POST["bid"]
        # Change the status of bidding in DB
        # and then save the latest status to DB
        listing.price = float(bid)
        listing.save()
        # Create bid use latest info
        Bid.objects.create(user=user, price=bid, listing=listing)

    return render(request, "auctions/list_details.html", {
        # ! Use same name for all the Key values.
        # lisitng: Show all listing ,
        "listing": listing,
        # catgory: item's catgory,
        "category": category,
        # comments: item's comments , for loop
        "comments": comments,
        # item be watched ?
        "watching": watch,
        # Is the owner are currently login ?
        "is_owner": is_owner
    })

# close_bidding Function


@login_required
def close_bidding(request, listing_id):
    # Get details from Listing DB function
    # ! Get necessary info from DB_Detail_Ref function just for Listing ONLY
    info = DB_Detail_Ref(request, listing_id)
    listing, user, is_owner, category, comments, watch = info[0], info[1], info[2], info[3], info[4], info[5]
    # Change the status of bidding in DB
    # and then save the latest status to DB
    listing.sold = True
    listing.save()
    # get winner and update winner
    winner = Bid.objects.get(price=listing.price, listing=listing).user
    is_winner = user.id == winner.id

    return render(request, "auctions/close_bidding.html", {
        # ! Use same name for all the Key values.
        # Value are extended from listing detail page,
        # lisitng: Show all listing ,
        "listing": listing,
        # catgory: item's catgory,
        "category": category,
        # comments: item's comments , for loop
        "comments": comments,
        # item be watched ?
        "watching": watch,
        # Is the owner are currently login ?
        "is_owner": is_owner,
        # Is the bid are the highest (Are you winner )?
        "is_winner": is_winner
    })

# ================================================
#               catgory Function
# ================================================


def category(request):
    listings = None
    category = None
    if request.method == "POST":
        # filter by catgory
        category = request.POST["categories"]
        listings = Listing.objects.filter(category=category)
    return render(request, "auctions/categories.html", {
        # Show Al  the categories
        "categories": Category.objects.all(),
        # get value by id when catgory is not None
        "category": Category.objects.get(id=category).category if category is not None else "",
        # then show listings
        "listing": listings
    })


@login_required
def Create_Catgory(request):
    if request.method == "POST":
        form = CreateCatgoryForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data["category"]
            Category.objects.create(category=category)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "auctions/create_catgory.html", {
            "create_catgory_form": CreateCatgoryForm(),
        })
