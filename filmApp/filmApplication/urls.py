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

    #Delete a director
    url(r'^directors/(?P<pk>\d+)/delete/$',
        DirectorDelete.as_view(model=Director),
        name='director_delete'),

    #List all directors
    url(r'^directors/$',
        DirectorList.as_view(),
        name='director_list'),

    # Director details: ex: /filmApplication/directors/40
    url(r'^directors/(?P<pk>\d+)/$',
        DirectorDetail.as_view(
            model = Director,
            template_name = 'directors_detail'
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

    #Delete Actor
    url(r'^actors/(?P<pk>\d+)/delete/$',
        ActorDelete.as_view(model=Actor),
        name='actor_delete'),

    #List all actors
    url(r'^actors/$',
        ActorList.as_view(),
        name='actor_list'),

    #Actor details: Ex: /filmApplication/actors/40
    url(r'^actors/(?P<pk>\d+)/$',
        ActorDetail.as_view(
            model = Actor,
            template_name = 'actors_detail'
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

    #Delete a movie
    url(r'^movies/(?P<pk>\d+)/delete/$',
        MovieDelete.as_view(model=Movie),
        name='movie_delete'),

    #List all movies : Ex: /filmApplication/films
    url(r'^movies/$',
        MovieList.as_view(),
        name='movie_list'),

    #Detail of a movie: /FilmApplication/films
    url(r'^movies/(?P<pk>\d+)/$',
        MovieDetail.as_view(
            model = Movie,
            template_name = 'movie_detail'
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

    #Delete a review of a movie
    url(r'^films/(?P<pkf>\d+)/reviews/(?P<pk>\d+)/delete/$',
        ReviewDelete.as_view(),
        name='score_delete'),

    #List all reviews of a movie
    url(r'^films/(?P<pkf>\d+)/reviews$',
        ReviewList.as_view(),
        name='review_list'),

    #Detail of a review of a particular movie
        url(r'^films/(?P<pkf>\d+)/review/(?P<pk>\d+)/$',
        ReviewDetail.as_view(
            model = MovieReview,
            template_name = 'review_detail'
        ),
        name='review_detail'),



)