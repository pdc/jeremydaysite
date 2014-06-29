# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import url
from django.conf import settings
import jeremyday.theweeklystrip.views
import jeremyday.theweeklystrip.rdf_views


urlpatterns = [
    url(r'^$', jeremyday.theweeklystrip.views.latest, {}, 'tws_latest'),
    url(r'^strips/(?P<number>[0-9]+)$', jeremyday.theweeklystrip.views.strip_page, {}, 'tws_strip'),
    url(r'^year/(?P<year>20[0-9]{2})$', jeremyday.theweeklystrip.views.year_page, {}, 'tws_year'),
    url(r'^bydate/(?P<year>20[0-9]{2})(?P<month>[01][0-9])(?P<day>[0-3][0-9])$', jeremyday.theweeklystrip.views.by_date, {}, 'tws_date'),
    url(r'^feeds/in-reading-order\.atom$', jeremyday.theweeklystrip.views.reading_order_feed, {}, 'tws_reading_order_feed'),
    url(r'^feeds/in-reading-order\.page(?P<page>[0-9]+)\.atom$', jeremyday.theweeklystrip.views.reading_order_feed, {}, 'tws_reading_order_feed'),

    url(r'^r/strip(?P<number>[0-9]+)$', jeremyday.theweeklystrip.rdf_views.strip_conneg, {}, 'tws_strip_resource'),
    url(r'^data/strip(?P<number>[0-9]+).(?P<format>n3|xml)$', jeremyday.theweeklystrip.rdf_views.strip_rdf, {}, 'tws_strip_rdf'),
]
