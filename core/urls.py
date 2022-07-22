from django.urls import path
from .views import *

# from rest_framework.authtoken import views

app_name = "shop"

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("profile/", UserDetailView.as_view(), name="profile"),
    path("login/", LoginUserAPIView.as_view(), name="login"),
    path("users/<int:pk>/", RetrieveUpdateDestroyUserView.as_view(), name="users"),
    path("create-auction/", CreateAuctionView.as_view(), name="create_auction"),
    path(
        "auction/<int:pk>/", RetrieveUpdateDestroyAuctionView.as_view(), name="auction"
    ),
    path("list-auction/", ListAuctionView.as_view(), name="auction_list"),
    path(
        "list-notcompleted-auction/",
        ListNotCompletedAuctionView.as_view(),
        name="auction_list",
    ),
    path("bidding-create/", BiddingCreateView.as_view(), name="bidding_create"),
]
