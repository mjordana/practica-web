# Create your views here.
from django.core import urlresolvers
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.template import Context
from models import Movie, Actor, Director, MovieReview,Review
from forms import MovieForm, DirectorForm, ActorForm, ReviewForm

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


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

# MOVIE:
class MovieDetail(LoginRequiredMixin,DetailView):
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


class MovieList(LoginRequiredMixin,ListView):
    model = Movie
    template_name = 'movie_list.html'
    queryset = Movie.objects.all()


#ACTORS
class ActorDetail(LoginRequiredMixin,DetailView):
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


class ActorList(LoginRequiredMixin,ListView):
    model = Actor
    template_name = 'actors_list.html'
    queryset = Actor.objects.all()


#DIRECTORS
class DirectorDetail(LoginRequiredMixin,DetailView):
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


class DirectorList(LoginRequiredMixin,ListView):
    model = Director
    template_name = 'directors_list.html'
    queryset = Director.objects.all()


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


def review(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    new_review = MovieReview(
        rating=request.POST['rating'],
        comment=request.POST['comment'],
        user=request.user,
        movie=movie,
    )
    new_review.save()
    return HttpResponseRedirect(urlresolvers.reverse('filmApplication:movie_detail', args=(movie.id,)))