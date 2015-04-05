import models
from django.contrib import admin

# Register your models here.
admin.site.register(models.Movie)
admin.site.register(models.Actor)
admin.site.register(models.Director)
admin.site.register(models.MovieReview)
admin.site.register(models.Genre)