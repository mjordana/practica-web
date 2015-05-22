from django.contrib.auth.models import User
from rest_framework import serializers
from filmApplication.models import Actor ,Director ,Movie,Genre,MovieReview
from rest_framework.relations import HyperlinkedRelatedField, HyperlinkedIdentityField
from rest_framework.fields import CharField


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email',)


class ActorSerializer(serializers.HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name='filmApplication:actor-detail')
    class Meta:
        model = Actor
        fields = ('url','name','birthYear', 'birthPlace','nationality',)


class DirectorSerializer(serializers.HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name='filmApplication:director-detail')
    class Meta:
        model = Director
        fields = ('url','name','birthYear', 'birthPlace','nationality',)


class MovieSerializer(serializers.HyperlinkedModelSerializer):

    url = HyperlinkedIdentityField(view_name='filmApplication:movie-detail')
    genre = HyperlinkedRelatedField(queryset=Genre.objects.all(),view_name='filmApplication:genres-detail')
    director = HyperlinkedRelatedField(queryset=Director.objects.all(),view_name='filmApplication:director-detail')
    actors = HyperlinkedRelatedField(many=True,queryset=Actor.objects.all(), view_name='filmApplication:actor-detail')

    class Meta:
        model = Movie
        fields = ('url','title','year', 'duration','genre','director','actors', )

class GenreSerializer(serializers.HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name='filmApplication:genres-detail')
    class Meta:
        model = Genre
        fields = ('url','genre',)

class MovieReviewSerializer(serializers.HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name='filmApplication:moviereview-detail')
    movie = HyperlinkedRelatedField(queryset = Movie.objects.all(), view_name='filmApplication:movie-detail')
    user = CharField(read_only=True)

    class Meta:
        model = MovieReview
        fields=('url','rating','comment','user','date','movie')




