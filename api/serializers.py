from rest_framework import serializers
from .models import Movie, Rating
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

##extra steps to secure the API. Restrict what can be viewed by certain users (permission classes)

# Used for the API view and what to show
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'description', 'num_of_ratings', 'avg_of_ratings') #num_of_ratings and avg_of_ratings comes from the Movie model's functions

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'movie', 'user', 'stars')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password') #need to pass in the password, but we will add other things to hide the password from the API call (or hash it)
        extra_kwargs = {'password': {'write_only': True, 'required': True}} #we won't be able to see it and will be required if we want to register a user

    def create(self, validated_data): ##this method was already there, but we override it for a custom version to not show the password
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user) ##create a token to the new registered user
        return user
