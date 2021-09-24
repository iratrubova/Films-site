from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", MoviesView.as_view(), name="movies"),
    path('', BaseView.as_view(), name='base'),
    path("filter/", FilterMoviesView.as_view(), name = 'filter'),
    path("search/", SearchView.as_view(), name = 'search'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path("<slug:slug>/", MoviesDetailView.as_view(), name='movie_detail'),
    path("review/<int:pk>/", AddReview.as_view(), name='add_review'),
    path("actor/<str:slug>/", ActorView.as_view(), name='actor_detail'),
    path("", BannerView.as_view()),

]