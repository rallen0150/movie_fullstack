# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=360)

    def __str__(self):
        return self.title

    def num_of_ratings(self):
        ratings = Rating.objects.filter(movie=self) #selecting all ratings belonging to this specific movie
        return len(ratings)

    def avg_of_ratings(self):
        sum = 0
        ratings = Rating.objects.filter(movie=self) #selecting all ratings belonging to this specific movie
        for rating in ratings:
            sum += rating.stars
        if len(ratings) > 0:
            return sum/len(ratings)
        else:
            return 0

class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE) #on_delete needs to be here since the movie is deleted and we don't want to break the code
    stars = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])

    def __str__(self):
        return self.movie.title+'-'+self.user.username

    class Meta:
        unique_together = (('user', 'movie'),) #this is to further limit only 1 rating on a movie by the user (a user can only rate once on a movie)
        index_together = (('user', 'movie'),) #this index_together is for explaining the path of how you get to the movie. First get the user, then the movie (in that order)
