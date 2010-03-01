from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('jeremyday.theweeklystrip.views',
    (r'^$', 'latest', {}, 'tws_latest'),
    (r'^strips/(?P<number>[0-9]+)$', 'strip_page', {}, 'tws_strip'),
    (r'^year/(?P<year>20[0-9]{2})$', 'year_page', {}, 'tws_year'),
    # Example:
    # (r'^jeremyday/', include('jeremyday.foo.urls')),
    
    #(r'^$', 'library_list', spreadlinks_args, 'library_list'),
)
