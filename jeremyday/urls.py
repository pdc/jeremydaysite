from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

spreadlinks_args = {
    'root_dir': settings.SPREADLINKS_DIR, 
    'template_name': 'jeremyday/projects_list.html',
}


urlpatterns = patterns('spreadsite.spreadlinks.views',
    (r'^(?P<library_name>projects)/$', 'library_detail', spreadlinks_args, 'library_detail'),
    (r'^(?P<library_name>projects)/page(?P<page>[0-9]+)$', 'library_detail', spreadlinks_args, 'library_detail'),
    (r'^(?P<library_name>projects)/tags/(?P<urlencoded_keywords>[a-z_0-9+:-]+)$', 'library_detail', spreadlinks_args, 'library_detail'),
    (r'^(?P<library_name>projects)/tags/(?P<urlencoded_keywords>[a-z_0-9+:-]+)/page(?P<page>[0-9]+)$', 'library_detail', spreadlinks_args, 'library_detail'),
) + patterns('jeremyday.frontpage.views',
    (r'^$', 'front_page', {}, 'front_page'),
    (r'^livejournal$', 'livejournal', {}, 'livejournal'),
) + patterns('',
    (r'^tws/', include('jeremyday.theweeklystrip.urls')),
    # Example:
    # (r'^jeremyday/', include('jeremyday.foo.urls')),
    
    #(r'^$', 'library_list', spreadlinks_args, 'library_list'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
