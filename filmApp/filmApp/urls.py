from django.conf.urls import patterns, include, url
from django.conf import settings
from filmApplication.views import *
from django.contrib import admin
admin.autodiscover()




urlpatterns = patterns('',

    url(r'^filmApplication/', include('filmApplication.urls', namespace='filmApplication')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    url(r'^register/$', register),
    url(r'^register/success/$', register_success),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', mainpage, name='home'),
)


if settings.DEBUG and settings.STATIC_ROOT:
    urlpatterns += patterns('',
        (r'%s(?P<path>.*)$' % settings.STATIC_URL.lstrip('/'), 
            'django.views.static.serve',
            {'document_root' : settings.STATIC_ROOT }),)
