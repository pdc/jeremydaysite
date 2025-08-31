"""
URL configuration for jeremydaysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import spreadlinks.views
from django.conf import settings
from django.urls import include, path

import jeremyday.frontpage.views
import jeremyday.theweeklystrip.urls

spreadlinks_args = {
    "root_dir": settings.SPREADLINKS_DIR,
    "library_name": "projects",
    "template_name": "jeremyday/projects_list.html",
}


urlpatterns = [
    # path("admin/", admin.site.urls),
    path(
        "projects/",
        spreadlinks.views.library_detail,
        spreadlinks_args,
        name="library_detail",
    ),
    path(
        "projects/page<int:page>",
        spreadlinks.views.library_detail,
        spreadlinks_args,
        name="library_detail",
    ),
    path(
        "projects/tags/<str:urlencoded_keywords>/",
        spreadlinks.views.library_detail,
        spreadlinks_args,
        name="library_detail",
    ),
    path(
        "projects/tags/<str:urlencoded_keywords>/page<int:page>",
        spreadlinks.views.library_detail,
        spreadlinks_args,
        name="library_detail",
    ),
    path("", jeremyday.frontpage.views.front_page, name="front_page"),
    path("livejournal", jeremyday.frontpage.views.livejournal, name="livejournal"),
    path("tws/", include(jeremyday.theweeklystrip.urls.urlpatterns)),
]
