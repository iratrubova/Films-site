from django.contrib import admin
from .models import Category, Actor, Genre, Movie, MovieShots, Rating, RatingStar, Reviews, Banner
from django.utils.safestring import mark_safe


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'id')



class ReviewInline(admin.StackedInline):
    model = Reviews
    extra = 1


class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width=120, height=80')
    get_image.short_description = 'Фото'

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('category','year')
    search_fields = ('title', 'category__name')
    inlines = [ MovieShotsInline, ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ('draft',)
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width=80, height=120')
    get_image.short_description = 'Фото'
   
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width=80, height=100')
    get_image.short_description = 'Фото'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'ip')

@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width=80, height=50')
    get_image.short_description = 'Фото'



admin.site.register(RatingStar)
admin.site.register(Reviews)
admin.site.register(Banner)
admin.site.site_title = "Марвел и DC фильмы"
admin.site.site_header = "Марвел и DC фильмы"