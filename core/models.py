from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)


class Auction(models.Model):
    """
    Auction Tabels
    """

    item_name = models.CharField(verbose_name="Item Name", max_length=120)
    start_price = models.PositiveIntegerField(verbose_name="Start Price")
    bidding = models.ForeignKey(
        "Bidding",
        verbose_name="Won Bidding",
        related_name="auctions",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    start_time = models.DateTimeField(verbose_name="Start Time")
    end_time = models.DateTimeField(verbose_name="End Time")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def is_completed(self):
        return timezone.now() > self.end_time

    def get_final_price(self):
        if self.bidding != None:
            return self.bidding.bidding_price
        else:
            return self.start_price

    def __str__(self):
        return f"{self.item_name} won by {self.get_final_price()}"


class Bidding(models.Model):
    """
    Bidding Table
    """

    auction = models.ForeignKey(
        Auction,
        related_name="biddings",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="biddings",
    )
    bidding_price = models.PositiveIntegerField(verbose_name="Bidding Price")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("bidding_price", "auction", "user")
