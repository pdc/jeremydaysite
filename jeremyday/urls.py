# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import url, include
from django.conf import settings
import spreadlinks.views
import jeremyday.frontpage.views


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

spreadlinks_args = {
    'root_dir': settings.SPREADLINKS_DIR,
    'template_name': 'jeremyday/projects_list.html',
}

urlpatterns = [
    url(r'^(?P<library_name>projects)/$', spreadlinks.views.library_detail, spreadlinks_args, 'library_detail'),
    url(r'^(?P<library_name>projects)/page(?P<page>[0-9]+)$', spreadlinks.views.library_detail, spreadlinks_args, 'library_detail'),
    url(r'^(?P<library_name>projects)/tags/(?P<urlencoded_keywords>[a-z_0-9+:-]+)$', spreadlinks.views.library_detail, spreadlinks_args, 'library_detail'),
    url(r'^(?P<library_name>projects)/tags/(?P<urlencoded_keywords>[a-z_0-9+:-]+)/page(?P<page>[0-9]+)$', spreadlinks.views.library_detail, spreadlinks_args, 'library_detail'),

    url(r'^$', jeremyday.frontpage.views.front_page, {}, 'front_page'),
    url(r'^livejournal$', jeremyday.frontpage.views.livejournal, {}, 'livejournal'),

    url(r'^tws/', include('jeremyday.theweeklystrip.urls')),

    # Example:
    # (r'^jeremyday/', include('jeremyday.foo.urls')),

    #(r'^$', 'library_list', spreadlinks_args, 'library_list'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
]
