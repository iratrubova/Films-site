from django.urls import path
from .views import *

urlpatterns = [
    path("", MoviesView.as_view()),
    path("<slug:slug>/", MoviesDetailView.as_view(), name='movie_detail'),
    path("review/<int:pk>/", AddReview.as_view(), name='add_review'),
    path("", BannerView.as_view()),

]