from django.urls import path

from . import views


from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    # index url
    path("", views.index, name="index"),
    # login url
    path("login", views.login_view, name="login"),
    # logout url
    path("logout", views.logout_view, name="logout"),
    # register url
    path("register", views.register, name="register"),
    # create listing url
    path("create", views.CreateListing, name="create"),
    # view Single lisitng by id
    path("list_details/<str:listing_id>", views.listing, name="listing"),
    # view Watched List by User id
    path("watch_list/<str:user_id>", views.watchlist, name="watchlist"),
    # Remove items from Watched List filltered by User id
    path("remove_watchlist/<str:listing_id>", views.remove_watchlist, name="remove_watchlist"),
    # Add items to Watched List filltered by User id
    path("add_watchlist/<str:listing_id>", views.add_watchlist, name="add_watchlist"),
    # Bid on individual item by list id
    path("bidding/<str:listing_id>", views.bidding, name="bidding"),
    # Close bid for individual item by list id
    path("close_bidding/<str:listing_id>", views.close_bidding, name="close_bidding"),
    # Show all items has catgoey field
    path("categories", views.category, name="categories"),
    path("create_catgory", views.Create_Catgory, name="create_catgory"),
]

urlpatterns += staticfiles_urlpatterns()
