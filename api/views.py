# -*- coding: utf-8 -*-
from __future__ import unicode_literals

## Import others for View specific functionality
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

## Import Models
from .models import Movie, Rating
from django.contrib.auth.models import User

## Import Serializers
from .serializers import MovieSerializer, RatingSerializer, UserSerializer

## Import User Token Auth
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, ) #only viewed by registered users

#These 2 are for the API view
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication, ) #must need to allow user create/updates from their tokens
    permission_classes = (AllowAny, ) #The movies API can be viewed by any one and not just by registered users

    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None): #this creates the rate_movie in the API url call for the specific movie you are rating based on the movie's id.   Ex: /api/movies/1/rate_movie

        #check if something has been passed in request
        if 'stars' in request.data:
            movie = Movie.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user #get the logged in user
            try:
                rating = Rating.objects.get(user=user.id, movie=movie.id) #trying to get the rating of a movie that the logged in user gave
                rating.stars = stars
                rating.save() #save the values to add to the api
                serializer = RatingSerializer(rating, many=False) #many false means only one object
                response = {'message': 'Rating Updated', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK) #if the results come back with a 200 status, then return the response
            except:
                rating = Rating.objects.create(user=user, movie=movie, stars=stars) #create a new rating object
                serializer = RatingSerializer(rating, many=False) #many false means only one object
                response = {'message': 'Rating Created', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK) #if the results come back with a 200 status, then return the response
        else:
            response = {'message': 'You need to provide stars.'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST) #If no stars, then come back with a bad request


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, ) #only viewed by registered users

    ## We are overriding the django pre-set updates and creates from their viewsets
    ## The reason this was added was because in this app we only want the user to create/update a rating through the 'rate_move' function in the MovieViewSet
    def update(self, request, *args, **kwargs):
        response = {'message': 'You cant update rating like that.'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    def create(self, request, *args, **kwargs):
        response = {'message': 'You cant create rating like that.'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
