from django.contrib import admin
from .models import *

class ListingAdmin(admin.ModelAdmin):
    list_display = ('creator', 'name', 'categories')

class BidAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'bidder', 'created_at')

admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Categories)
admin.site.register(Bid, BidAdmin)

