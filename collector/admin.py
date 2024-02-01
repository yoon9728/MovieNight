from django.contrib import admin
from .models import Movie, Genre, Actor, Director

class GenreInline(admin.TabularInline):
    model = Movie.genres.through  

class MovieAdmin(admin.ModelAdmin):
    inlines = [GenreInline]

admin.site.register(Movie, MovieAdmin)

admin.site.register(Genre)

admin.site.register(Actor)

admin.site.register(Director)