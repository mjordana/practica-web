from django.forms import ModelForm
from filmApplication.models import Movie, Director, Actor, Review

class MovieForm(ModelForm):
    class Meta:
        model = Movie
        exclude = ('user',)

class DirectorForm(ModelForm):
    class Meta:
        model = Director
        exclude = ('user',)

class ActorForm(ModelForm):
    class Meta:
        model = Actor
        exclude = ('user',)

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        exclude = ('user','date',)