from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('jeremyday.theweeklystrip.views',
    (r'^$', 'latest', {}, 'tws_latest'),
    (r'^strips/(?P<number>[0-9]+)$', 'strip_page', {}, 'tws_strip'),
    # Example:
    # (r'^jeremyday/', include('jeremyday.foo.urls')),
    
    #(r'^$', 'library_list', spreadlinks_args, 'library_list'),
)
