from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Actor(models.Model):
    name = models.TextField(max_length = 50)
    birthYear = models.IntegerField()
    birthPlace = models.TextField(max_length = 50)
    nationality = models.TextField(max_length = 15)

    def __unicode__(self):
        return u"%s" % self.name

    def get_absolute_url(self):
        return reverse('filmApplication:actor_detail',kwargs={'pk':self.pk})


class Director(models.Model):
    name = models.TextField(max_length = 50)
    birthYear = models.IntegerField()
    birthPlace = models.TextField(max_length = 50)
    nationality = models.TextField(max_length = 15)

    def __unicode__(self):
        return u"%s" % self.name

    def get_absolute_url(self):
        return reverse('filmApplication:director_detail',kwargs={'pk':self.pk})


class Genre(models.Model):
    tipus = (('comedy','comedy'),('action','action'),('drama','drama'),('terror','terror'),
        ('fantasy','fantasy'),('thriller','thriller'),('aventura','aventura'),('scienceFiction','scienceFiction'),
	    ('western','western'))
    genre = models.CharField(max_length=15,choices=tipus,unique=True)

    def __unicode__(self):
        return u"%s" % self.genre

    def get_absolute_url(self):
        return reverse('filmApplication:genres_detail',kwargs={'pk':self.pk})

class Movie(models.Model):
    title = models.TextField(max_length = 50)
    year = models.IntegerField()
    duration = models.IntegerField()
    genre = models.ForeignKey(Genre)
    director = models.ForeignKey(Director)
    actors = models.ManyToManyField(Actor)

    def __unicode__(self):
        return u"%s" % self.title

    def get_absolute_url(self):
        return reverse('filmApplication:movie_detail',kwargs={'pk':self.pk})



class Review(models.Model):

    RATING_CHOICES = ((1,'1'), (2,'2'), (3,'3'), (4,'4'), (5,'5'))
    rating = models.PositiveSmallIntegerField('rating (stars)', blank=False, default=3,
		choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, default=1)
    date = models.DateField(default=date.today)

    class Meta:
        abstract = True


class MovieReview(Review):
    movie = models.ForeignKey(Movie)
    def get_absolute_url(self):
        return reverse('filmApplication:movie_detail',kwargs={'pk':self.movie.pk})


