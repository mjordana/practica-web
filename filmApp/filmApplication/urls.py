from django.conf import settings
from django.conf.urls import patterns, include, url
from filmApplication.models import Actor, Director, Movie, Genre
from filmApplication.forms import ActorForm, DirectorForm, MovieForm, ReviewForm
from filmApplication.views import *
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',

#DIRECTORS urls

    # Create a new Director : ex: /filmApplication/directors/create
    url(r'^directors/create/$',
        DirectorCreate.as_view(),
        name='director_create'),

    #Edit director details, ex: filmApplication/directors/40/edit
    url(r'^directors/(?P<pk>\d+)/edit/$',
        DirectorUpdate.as_view(
            model=Director,
            form_class=DirectorForm,
            template_name='form.html'
        ),
        name= 'director_edit'),

    #List all directors
    url(r'^directors\.(?P<extension>(json|xml))$',
        DirectorList.as_view(),
        name='directors_list_conneg'),

    #List all directors
    url(r'^directors/$',
        DirectorList.as_view(),
        name='directors_list'),

    # Director details: ex: /filmApplication/directors/40
    url(r'^directors/(?P<pk>\d+)\.(?P<extension>(json|xml))$',
        DirectorDetail.as_view(
            model = Director,
        ),
        name='director_detail_conneg'),

    # Director details: ex: /filmApplication/directors/40
    url(r'^directors/(?P<pk>\d+)/$',
        DirectorDetail.as_view(
            model = Director,
            template_name = 'director_detail.html'
        ),
        name='director_detail'),

    url(r'^directors/(?P<pk>\d+)/delete/$',
        DirectorDelete.as_view(
            model = Director,
            template_name = 'delete.html'
        ),
        name = 'delete_director'),

#ACTORS urls

    #Create new actor
    url(r'^actors/create/$',
        ActorCreate.as_view(),
        name='actor_create'),

    #Edit actor details, ex: filmApplication/actors/30/edit
    url(r'^actors/(?P<pk>\d+)/edit/$',
        ActorUpdate.as_view(
            model=Actor,
            form_class=ActorForm,
            template_name='form.html'
        ),
        name='actor_edit'),

    #List all actors
    url(r'^actors\.(?P<extension>(json|xml))/$',
        ActorList.as_view(),
        name='actors_list_conneg'),

    url(r'^actors/$',
        ActorList.as_view(),
        name='actors_list'),

    url(r'^actors/(?P<pk>\d+)\.(?P<extension>(json|xml))$',
        ActorDetail.as_view(
            model = Actor,
        ),
        name='actor_detail_conneg'),

    #Actor details: Ex: /filmApplication/actors/40
    url(r'^actors/(?P<pk>\d+)/$',
        ActorDetail.as_view(
            model = Actor,
            template_name = 'actor_detail.html'
        ),
        name='actor_detail'),

    url(r'^actors/(?P<pk>\d+)/delete/$',
        ActorDelete.as_view(
            model = Actor,
            template_name = 'delete.html'
        ),
        name = 'delete_actor'),


    url(r'^genres\.(?P<extension>(json|xml))$',
        GenreList.as_view(),
        name='genres_list_conneg'),


    url(r'^genres/$',
        GenreList.as_view(),
        name='genres_list'),


    #Detail of a genre: Movies of a concrete genre
    url(r'^genres/(?P<pk>\d+)\.(?P<extension>(json|xml))$',
        GenreDetail.as_view(
            model = Genre,
        ),
        name='genres_detail_conneg'),

    #Detail of a genre: Movies of a concrete genre
    url(r'^genres/(?P<pk>\d+)/$',
        GenreDetail.as_view(
            model = Genre,
            template_name = 'genres_detail.html',
        ),
        name='genres_detail'),

#MOVIES urls

    #Create new movie
    url(r'^movies/create/$',
        MovieCreate.as_view(),
        name='movie_create'),

    #Edit a movie: Ex: /filmApplication/films/123/edit
    url(r'^movies/(?P<pk>\d+)/edit/$',
        MovieUpdate.as_view(
            model = Movie,
            form_class = MovieForm,
            template_name = 'form.html'
        ),
        name='movie_edit'),


    #List all movies : Ex: /filmApplication/films
    url(r'^movies\.(?P<extension>(json|xml))$',
        MovieList.as_view(),
        name='movie_list_conneg'),

    #List all movies : Ex: /filmApplication/films
    url(r'^movies/$',
        MovieList.as_view(),
        name='movie_list'),


    url(r'^movies/(?P<pk>\d+)\.(?P<extension>(json|xml))$',
        MovieDetail.as_view(
            model = Movie,
        ),
        name='movie_detail_conneg'),

    #Detail of a movie: /FilmApplication/films
    url(r'^movies/(?P<pk>\d+)/$',
        MovieDetail.as_view(
            model = Movie,
            template_name = 'movie_detail.html'
        ),
        name='movie_detail'),


    url(r'^movies/(?P<pk>\d+)/delete/$',
        MovieDelete.as_view(
            model = Movie,
            template_name = 'delete.html'
        ),
        name = 'delete_movie'),

#SCORE urls

    #Create new review
    url(r'^movies/(?P<pk>\d+)/create_review/$',
        'filmApplication.views.review',

        name='review_create'),

    #Edit a review of a movie if we are the owners
    url(r'^reviews/(?P<pk>\d+)/edit/$',
        ReviewUpdate.as_view(
            model=MovieReview,
            form_class=ReviewForm,
            template_name = 'form.html'
        ),
        name='review_edit'),

    #Delete a review of a movie if we are the owners
    url(r'^reviews/(?P<pk>\d+)/delete/$',
        MovieDelete.as_view(
            model = MovieReview,
            template_name = 'delete.html'
        ),
        name = 'delete_review'),
)