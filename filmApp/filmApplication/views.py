# Create your views here.
from django.core import urlresolvers
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response,render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.template import Context
from rest_framework.reverse import reverse
from rest_framework.response import Response
from django.views.generic.base import TemplateResponseMixin
from django.core import serializers

from models import Movie, Actor, Director, MovieReview,Review,Genre
from forms import MovieForm, DirectorForm, ActorForm, ReviewForm,RegistrationForm

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.contrib.auth import logout
from rest_framework.decorators import api_view

from rest_framework import viewsets
from rest_framework import generics
from filmApplication.serializers import UserSerializer,MovieSerializer, ActorSerializer, DirectorSerializer, MovieReviewSerializer, GenreSerializer

#Per assegurar-nos que estem loggejats al entrar en una URL
class LoginRequiredMixin(object):
    """Ensures that user must be authenticated in order to access view."""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class ConnegResponseMixin(TemplateResponseMixin):

    def render_json_object_response(self, objects, **kwargs):
        json_data = serializers.serialize(u"json", objects, **kwargs)
        return HttpResponse(json_data, content_type=u"application/json")

    def render_xml_object_response(self, objects, **kwargs):
        xml_data = serializers.serialize(u"xml", objects, **kwargs)
        return HttpResponse(xml_data, content_type=u"application/xml")

    def render_to_response(self, context, **kwargs):
        if 'extension' in self.kwargs:
            try:
                objects = [self.object]
            except AttributeError:
                objects = self.object_list
            if self.kwargs['extension'] == 'json':
                return self.render_json_object_response(objects=objects)
            elif self.kwargs['extension'] == 'xml':
                return self.render_xml_object_response(objects=objects)
        else:
            return super(ConnegResponseMixin, self).render_to_response(context)

def mainpage(request):
    template = get_template('mainpage.html')
    variables = Context({
        'titlehead': 'Movie Application',
        'pagetitle': 'Welcome to the New Movie Application',
        'contentbody': 'A new page made by US since 2015',
        'user': request.user,
        'main':'true',
    })
    output = template.render(variables)
    return HttpResponse(output)

#REST FRAMEWORK PART:

@api_view(['GET'])
def api_root(request, format=None):
    """
    The entry endpoint of our API
    """
    return Response({
        'users': reverse('user-list', vrequest=request),
        'movies': reverse('movies-list', request=request),
        'actors': reverse('actors-list', request=request),
        'directors': reverse('directors-list', request=request),
        'reviews': reverse('reviews-list', request=request),
        'genres': reverse('genres-list', request=request),
    })

class APIMovieList(generics.ListCreateAPIView):
    model = Movie
    serializer_class = MovieSerializer


class APIMovieDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Movie
    serializer_class = MovieSerializer


class APIMovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class APIActorList(generics.ListCreateAPIView):
    model = Actor
    serializer_class = ActorSerializer


class APIActorDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Actor
    serializer_class = ActorSerializer


class APIActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class APIDirectorList(generics.ListCreateAPIView):
    model = Director
    serializer_class = DirectorSerializer


class APIDirectorDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Movie
    serializer_class = DirectorSerializer


class APIDirectorViewSet(viewsets.ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

class APIReviewViewSet(viewsets.ModelViewSet):
    queryset = MovieReview.objects.all()
    serializer_class = MovieReviewSerializer

class APIReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    model = MovieReview
    serializer_class = MovieReviewSerializer

class APIGenreList(generics.ListCreateAPIView):
    model = Genre
    serializer_class = GenreSerializer

class APIGenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


#------------------------------------------------------------------

# MOVIE:
class MovieDetail(LoginRequiredMixin,DetailView,ConnegResponseMixin):
    model = Movie
    template_name ="movie_detail.html"

    def get_context_data(self, **kwargs):
        context = super(MovieDetail, self).get_context_data(**kwargs)
        context['RATING_CHOICES'] = Review.RATING_CHOICES
        context['average'] = self.get_average_rating()
        return context

    def get_average_rating(self):
        total = 0
        reviews = self.get_reviews()
        for rev in reviews:
            total += rev.rating

        av = total/float(len(reviews))
        dec =  float("{0:.2f}".format(av))

        return dec

    def get_reviews(self):
        return MovieReview.objects.filter(movie__id=self.kwargs['pk'])


class MovieCreate(LoginRequiredMixin,CreateView):
    model = Movie
    template_name = 'form.html'
    form_class = MovieForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(MovieCreate, self).form_valid(form)


class MovieUpdate(LoginRequiredMixin,UpdateView):
    model = Movie
    template_name = 'update.html'


class MovieList(LoginRequiredMixin,ListView,ConnegResponseMixin):
    model = Movie
    template_name = 'movie_list.html'
    queryset = Movie.objects.all()

class MovieDelete(LoginRequiredMixin,DeleteView):
    model = Movie
    template_name = 'delete.html'
    success_url = '/filmApplication/movies/'

#ACTORS
class ActorDetail(LoginRequiredMixin,DetailView,ConnegResponseMixin):
    model = Actor
    template_name = 'actor_detail.html'


class ActorCreate(LoginRequiredMixin,CreateView):
    model = Actor
    template_name = 'form.html'
    form_class = ActorForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ActorCreate, self).form_valid(form)


class ActorUpdate(LoginRequiredMixin,UpdateView):
    model = Actor
    template_name = 'update.html'


class ActorList(LoginRequiredMixin,ListView,ConnegResponseMixin):
    model = Actor
    template_name = 'actors_list.html'
    queryset = Actor.objects.all()


class ActorDelete(LoginRequiredMixin,DeleteView):
    model = Actor
    template_name = 'delete.html'
    success_url = '/filmApplication/actors/'


#DIRECTORS
class DirectorDetail(LoginRequiredMixin,DetailView,ConnegResponseMixin):
    model = Director
    template_name = 'director_detail.html'


class DirectorCreate(LoginRequiredMixin,CreateView):
    model = Director
    template_name = 'form.html'
    form_class = DirectorForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(DirectorCreate, self).form_valid(form)


class DirectorUpdate(LoginRequiredMixin,UpdateView):
    model = Director
    template_name = 'update.html'


class DirectorList(LoginRequiredMixin,ListView,ConnegResponseMixin):
    model = Director
    template_name = 'directors_list.html'
    queryset = Director.objects.all()

class DirectorDelete(LoginRequiredMixin,DeleteView):
    model = Director
    template_name = 'delete.html'
    success_url = '/filmApplication/directors/'


#SCORE:
class ReviewCreate(LoginRequiredMixin,CreateView):
    model = MovieReview
    template_name = 'form.html'
    form_class = ReviewForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.movie = Movie.objects.get(id=self.kwargs['pk'])
        return super(ReviewCreate, self).form_valid(form)


class ReviewUpdate(LoginRequiredMixin,UpdateView):
    model = MovieReview
    template_name = 'update.html'

class ReviewDelete(LoginRequiredMixin,DeleteView):
    model = MovieReview
    template_name = 'delete.html'


def review(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    new_review = MovieReview(
        rating = request.POST['rating'],
        comment = request.POST['comment'],
        user = request.user,
        movie = movie
    )
    new_review.save()
    return HttpResponseRedirect(urlresolvers.reverse('filmApplication:movie_detail', args=(movie.id,)))


#GENRES : Only admin create and delete genres not users
class GenreList(LoginRequiredMixin, ListView, ConnegResponseMixin):
    model = Genre
    template_name = 'genres_list.html'
    queryset = Genre.objects.all()



class GenreDetail(LoginRequiredMixin, DetailView, ConnegResponseMixin):
    model = Genre

    def get(self, request, *args, **kwargs):
        return render(request, self.get_template_name(),self.get_context_data())

    def get_template_name(self):
        return 'genres_detail.html'

    def get_context_data(self):
        return {'queryset': self.get_object()}

    def get_object(self):
        return Movie.objects.filter(genre__id=self.kwargs['pk'])


#-------------------------------------------------------------------
#REGISTER PART
@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })

    return render_to_response(
    'registration/register.html',
    variables,
    )

def register_success(request):
    return render_to_response(
    'registration/success.html',
    )

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


#..............................................

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    model = User
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    model = User
    serializer_class = UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
