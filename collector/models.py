from django.db import models
from django.utils import timezone

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Actor(models.Model):
    Actor_id = models.CharField(max_length=100, unique=True, null=True)
    name = models.CharField(max_length=100)
    profile_image = models.URLField(null=True)

    def __str__(self):
        return self.name if self.name else "Unknown Director"

class Director(models.Model):
    Director_id = models.CharField(max_length=100, unique=True, null=True)
    name = models.CharField(max_length=100, null = True)
    profile_image = models.URLField(null=True)

    def __str__(self):
        return self.name if self.name else "Unknown Director"

class Movie(models.Model):
    TMDB_id = models.CharField(max_length=200, null=True, unique=True)
    title = models.CharField(max_length=200)
    director = models.ForeignKey(Director, on_delete=models.CASCADE) 
    genres = models.ManyToManyField(Genre)
    poster_url = models.URLField(null=True)
    release_date = models.DateField(default=timezone.now, null=True)
    popularity = models.IntegerField(null=True)
    IMDB_id = models.CharField(max_length=100, null=True)
    IMDB_rating = models.CharField(max_length=100, null=True)
    overview = models.CharField(max_length=700, null=True)
    lead_actors = models.ManyToManyField(Actor) 
    runtime = models.CharField(max_length=50, null=True)
    trailer_url = models.URLField(null=True)


    def __str__(self):
        return self.title
