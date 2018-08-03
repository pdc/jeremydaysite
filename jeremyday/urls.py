# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import include, url
from django.conf import settings
import spreadlinks.views
import jeremyday.frontpage.views
import jeremyday.theweeklystrip.urls


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

spreadlinks_args = {
    'root_dir': settings.SPREADLINKS_DIR,
    'library_name': 'projects',
    'template_name': 'jeremyday/projects_list.html',
}

spreadlinks_patterns = [
    url(x, spreadlinks.views.library_detail, spreadlinks_args, name='library_detail')
    for x in [r'^$', r'^page(?P<page>\d+)$']
]

urlpatterns = [
    url(r'^projects/', include(
        spreadlinks_patterns + [
        url(r'^tags/(?P<urlencoded_keywords>[a-z_0-9+:-]+)', include(spreadlinks_patterns)),
    ])),

    url(r'^$', jeremyday.frontpage.views.front_page, name='front_page'),
    url(r'^livejournal$', jeremyday.frontpage.views.livejournal, name='livejournal'),
    url(r'^tws/', include(jeremyday.theweeklystrip.urls.urlpatterns)),
]

# urlpatterns = [
#     url(r'^(?P<library_name>projects)/$', spreadlinks.views.library_detail, spreadlinks_args, 'library_detail'),
#     url(r'^(?P<library_name>projects)/page(?P<page>[0-9]+)$', spreadlinks.views.library_detail, spreadlinks_args, 'library_detail'),
#     url(r'^(?P<library_name>projects)/tags/(?P<urlencoded_keywords>[a-z_0-9+:-]+)$', spreadlinks.views.library_detail, spreadlinks_args, 'library_detail'),
#     url(r'^(?P<library_name>projects)/tags/(?P<urlencoded_keywords>[a-z_0-9+:-]+)/page(?P<page>[0-9]+)$', spreadlinks.views.library_detail, spreadlinks_args, 'library_detail'),

#     url(r'^$', jeremyday.frontpage.views.front_page, {}, 'front_page'),
#     url(r'^livejournal$', jeremyday.frontpage.views.livejournal, {}, 'livejournal'),

#     url(r'^tws/', include(jeremyday.theweeklystrip.urls.url_patterns)),
# ]
