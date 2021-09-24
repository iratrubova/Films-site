from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django import views
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from .models import Movie, Banner, MovieShots, Category, Actor, Genre, RatingStar, Rating
from .forms import ReviewsForm, RatingForm, LoginForm, RegistrationForm
from django.db.models import Q



class BaseView(views.View):

    def get(self, request, *args, **kwargs):
        return render(request, 'base.html', {})

class GenreYear:

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year")

class MoviesView(GenreYear, ListView):

    model = Movie

    queryset = Movie.objects.filter(draft=False)
    template_name = 'movies/movies.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all()
        return context


class MoviesDetailView(GenreYear, DetailView):

    model = Movie
    slug_field = 'url'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        return context


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


class ActorView(DetailView):
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = 'name'

class FilterMoviesView(GenreYear, ListView):
    template_name = "movies/movies.html"

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year"))| 
            Q(genres__in=self.request.GET.getlist("genre"))
            )
        return queryset





class SearchView(ListView):
   
    template_name = 'movies/movies.html'

    def get_queryset(self):
        q = self.request.GET.get('q')
        a = "".join(q[0].upper()) + q[1:]
        return Movie.objects.filter(title__icontains=a)
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = self.request.GET.get('q')
        return context


class LoginView(views.View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'login.html', context)

class RegistrationView(views.View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')

        context = {
            'form': form
        }
        return render(request, 'registration.html', context)
       



