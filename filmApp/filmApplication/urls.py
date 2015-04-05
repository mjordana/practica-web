from django.conf.urls import patterns, include, url
from filmApplication.models import Actor, Director, Movie
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
    url(r'^directors/$',
        DirectorList.as_view(),
        name='directors_list'),

    # Director details: ex: /filmApplication/directors/40
    url(r'^directors/(?P<pk>\d+)/$',
        DirectorDetail.as_view(
            model = Director,
            template_name = 'director_detail.html'
        ),
        name='director_detail'),

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
    url(r'^actors/$',
        ActorList.as_view(),
        name='actors_list'),

    #Actor details: Ex: /filmApplication/actors/40
    url(r'^actors/(?P<pk>\d+)/$',
        ActorDetail.as_view(
            model = Actor,
            template_name = 'actor_detail.html'
        ),
        name='actor_detail'),


    #MOVIES urls

    #Create new movie
    url(r'^movies/create/$',
        MovieCreate.as_view(),
        name='movie_create'),

    #Edit a movie: Ex: /filmApplication/films/123/edit
    url(r'^movies/(?P<pk>\d+)/edit/$',
        MovieUpdate.as_view(
            model=Movie,
            form_class=MovieForm,
            template_name = 'form.html'
        ),
        name='movie_edit'),


    #List all movies : Ex: /filmApplication/films
    url(r'^movies/$',
        MovieList.as_view(),
        name='movie_list'),

    #Detail of a movie: /FilmApplication/films
    url(r'^movies/(?P<pk>\d+)/$',
        MovieDetail.as_view(
            model = Movie,
            template_name = 'movie_detail.html'
        ),
        name='movie_detail'),


    #SCORE urls

    #Create new review
    url(r'^films/(?P<pk>\d+)/review/create/$',
        'filmApplication.views.review',
        name='review_create'),

    #Edit a review of a movie
    url(r'^films/(?P<pkf>\d+)/reviews/(?P<pk>\d+)/edit/$',
        ReviewUpdate.as_view(
            model=MovieReview,
            form_class=ReviewForm,
            template_name = 'form.html'
        ),
        name='score_edit'),




)