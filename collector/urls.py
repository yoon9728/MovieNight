from django.urls import path
from .views import HomePage, load_more_movies, load_movies, About


from . import views

app_name = "collector"

urlpatterns = [
    path("", views.HomePage.as_view(), name="index"),
    path('load-movies', views.load_movies, name='load-movies'),
    path('load-more-movies', views.load_more_movies, name='load-more-movies'),
    path("todaysPick", views.todaysPick.as_view(), name="todaysPick"),
    path('about/', views.About.as_view(), name='about'),

]
