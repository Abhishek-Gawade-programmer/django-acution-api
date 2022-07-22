from django.shortcuts import render
from .models import Auction, Bidding
from .serializers import *
from .permissions import IsAdministerUser
from django.utils import timezone

# rest imports
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token


class UserCreateView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer


class CreateAuctionView(generics.CreateAPIView):
    serializer_class = AuctionSerializer
    permission_classes = [IsAuthenticated, IsAdministerUser]


class RetrieveUpdateDestroyAuctionView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AuctionSerializer
    queryset = Auction.objects.all()
    permission_classes = [IsAuthenticated, IsAdministerUser]


class ListAuctionView(generics.ListAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    permission_classes = [IsAuthenticated, IsAdministerUser]


class ListNotCompletedAuctionView(generics.ListAPIView):
    queryset = Auction.objects.filter(end_time__lt=timezone.now())
    serializer_class = AuctionSerializer
    permission_classes = [IsAuthenticated]


class RetrieveUpdateDestroyUserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdministerUser]
    queryset = User.objects.all()


class LoginUserAPIView(APIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        # get user token
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)


class BiddingCreateView(generics.CreateAPIView):
    serializer_class = BiddingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        # Setting the bid value to max bid apllied
        if instance.bidding_price >= instance.auction.get_final_price():
            instance.auction.bidding = instance
            instance.auction.save()


class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
