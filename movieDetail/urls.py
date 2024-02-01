from django.urls import path
from .views import MovieDetailView

app_name = 'movieDetail'

urlpatterns = [
    path('<str:title>/<int:tmdb_id>/', MovieDetailView.as_view(), name='movie_detail'),
]
