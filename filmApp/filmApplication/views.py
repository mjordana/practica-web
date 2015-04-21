# Create your views here.
from django.core import urlresolvers
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response,render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.template import Context

from models import Movie, Actor, Director, MovieReview,Review,Genre
from forms import MovieForm, DirectorForm, ActorForm, ReviewForm,RegistrationForm
from django.views.generic.base import TemplateResponseMixin,TemplateResponse
from django.core import serializers

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.contrib.auth import logout


class LoginRequiredMixin(object):
    """Ensures that user must be authenticated in order to access view."""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


#Primer exemple de pagina principal
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


#Parser to XML and JSON
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


# MOVIE:
class MovieDetail(LoginRequiredMixin,DetailView, ConnegResponseMixin):
    model = Movie
    template_name = 'movie_detail.html'

    def get_context_data(self, **kwargs):
        context = super(MovieDetail, self).get_context_data(**kwargs)
        context['RATING_CHOICES'] = Review.RATING_CHOICES
        return context


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

@login_required
def home(request):
    return render_to_response(
    'mainpage.html',
    { 'user': request.user }
    )

