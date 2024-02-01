
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from collector.models import Movie

class MovieDetailView(DetailView):
    model = Movie
    template_name = 'detail/moviedetail.html'
    context_object_name = 'movie'

    def get_object(self):
        tmdb_id = self.kwargs.get('tmdb_id')
        return get_object_or_404(Movie, TMDB_id=tmdb_id)
