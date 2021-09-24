from django.shortcuts import render, redirect
from django import views
from django.views.generic import ListView, DetailView
from .models import Movie, Banner, MovieShots
from .forms import ReviewsForm

class MoviesView(ListView):

    model = Movie

    queryset = Movie.objects.filter(draft=False)
    template_name = 'movies/movies.html'


class MoviesDetailView(DetailView):

    model = Movie
    slug_field = 'url'

class BannerView(views.View):

    def get(self, request):
        banner = Banner.objects.all()
        return render(request, 'movies/movies.html', {'banner': banner})


class AddReview(views.View):
    def post(self, request, pk):

        form = ReviewsForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie_id = pk
            form.save()
        return redirect(movie.get_absolute_url())


