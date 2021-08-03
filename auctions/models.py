from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE


class Listing(models.Model):
    creator = models.ForeignKey('User', on_delete=CASCADE)
    categories = models.ForeignKey('Categories', on_delete=CASCADE, blank=True, null=True)
    name = models.CharField(max_length=75, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    image = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True)
    current_price = models.ForeignKey("Bid", blank=True, null=True, on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


    def __str__(self):
        return self.name


class User(AbstractUser):
    pass
    



class Categories(models.Model):
    title = models.CharField(max_length=75)
    
    def __str__(self):
        return self.title


class Bid(models.Model):
    name = models.ForeignKey("Listing", on_delete=CASCADE)
    bidder = models.ForeignKey("User", on_delete=CASCADE, null=True)
    price = models.FloatField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.price}"



class Watchlist(models.Model):
    user = models.ForeignKey("User", on_delete=CASCADE, null=True)
    listings = models.ForeignKey("Listing", null=True, blank=True, on_delete=CASCADE)

    def __str__(self):
        return f"{self.user} -- {self.listings}"