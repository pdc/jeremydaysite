from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('jeremyday.theweeklystrip.views',
    (r'^$', 'latest', {}, 'tws_latest'),
    (r'^strips/(?P<number>[0-9]+)$', 'strip_page', {}, 'tws_strip'),
    (r'^year/(?P<year>20[0-9]{2})$', 'year_page', {}, 'tws_year'),
    (r'^bydate/(?P<year>20[0-9]{2})(?P<month>[01][0-9])(?P<day>[0-3][0-9])$', 'by_date', {}, 'tws_date'),
    (r'^feeds/in-reading-order\.atom$', 'reading_order_feed', {}, 'tws_reading_order_feed'),
    (r'^feeds/in-reading-order\.page(?P<page>[0-9]+)\.atom$', 'reading_order_feed', {}, 'tws_reading_order_feed'),
    # Example:
    # (r'^jeremyday/', include('jeremyday.foo.urls')),
    
    #(r'^$', 'library_list', spreadlinks_args, 'library_list'),
) + patterns('jeremyday.theweeklystrip.rdf_views',
    (r'^r/strip(?P<number>[0-9]+)$', 'strip_conneg', {}, 'tws_strip_resource'),
    (r'^data/strip(?P<number>[0-9]+).(?P<format>n3|xml)$', 'strip_rdf', {}, 'tws_strip_rdf'),
)
