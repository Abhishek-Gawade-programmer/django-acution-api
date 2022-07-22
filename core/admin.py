from django.contrib import admin
from .models import User, Auction, Bidding

admin.site.register(User)
admin.site.register(Auction)
admin.site.register(Bidding)

# Register your models here.
