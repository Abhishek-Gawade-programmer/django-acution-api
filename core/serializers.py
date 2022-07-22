from rest_framework import serializers
from .models import User, Auction, Bidding
from django.contrib.auth import authenticate
from rest_framework import exceptions


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")


class BiddingSerializer(serializers.ModelSerializer):
    auction = serializers.PrimaryKeyRelatedField(queryset=Auction.objects.all())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Bidding
        fields = ("id", "auction", "user", "bidding_price", "created", "updated")

    def validate_auction(self, value):
        if value.is_completed():
            raise exceptions.ValidationError("Auction is already Completed or Ended")
        return value

    def validate(self, data):
        if data.get("bidding_price") < data.get("auction").start_price:
            raise exceptions.ValidationError(
                "Minimun Value Should me more than "
                + str(data.get("auction").start_price)
            )
        return data


class AuctionSerializer(serializers.ModelSerializer):
    bidding = BiddingSerializer(read_only=True)
    is_completed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Auction
        fields = (
            "id",
            "item_name",
            "start_price",
            "bidding",
            "start_time",
            "end_time",
            "is_completed",
            "created",
            "updated",
        )

    def get_is_completed(self, obj):
        return obj.is_completed()

    def validate(self, data):
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        if start_time > end_time:
            raise exceptions.ValidationError(
                "Please Enter Valid Time Between start_time end_time"
            )
        return data


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            data["user"] = user
            return data
        else:
            raise exceptions.ValidationError("Unable to login with given credentials.")
