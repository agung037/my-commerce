from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:pk>", views.listing, name="listing"),
    path("listing/create", views.create_listing_view, name="createListing"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("watchlist/<int:pk>", views.watchlist_edit, name="watchlist"),
    path("category/<int:pk>", views.category, name="category"),
    path("listingstatus/<int:pk>", views.listing_status, name="listingStatus"),
    path("comment/<int:pk>", views.comment, name="comment"),
]
