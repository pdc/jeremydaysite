# -*- coding: utf-8 -*-


from django.urls import path, re_path

import jeremyday.theweeklystrip.rdf_views
import jeremyday.theweeklystrip.views

urlpatterns = [
    path(r"", jeremyday.theweeklystrip.views.latest, name="tws_latest"),
    path(
        r"strips/<int:number>",
        jeremyday.theweeklystrip.views.strip_page,
        name="tws_strip",
    ),
    path(
        r"year/<int:year>",
        jeremyday.theweeklystrip.views.year_page,
        name="tws_year",
    ),
    re_path(
        r"^bydate/(?P<year>20[0-9]{2})(?P<month>[01][0-9])(?P<day>[0-3][0-9])$",
        jeremyday.theweeklystrip.views.by_date,
        name="tws_date",
    ),
    path(
        r"feeds/in-reading-order.atom",
        jeremyday.theweeklystrip.views.reading_order_feed,
        name="tws_reading_order_feed",
    ),
    path(
        r"feeds/in-reading-order.page<int:page>.atom",
        jeremyday.theweeklystrip.views.reading_order_feed,
        name="tws_reading_order_feed",
    ),
    path(
        r"r/strip<int:number>",
        jeremyday.theweeklystrip.rdf_views.strip_conneg,
        name="tws_strip_resource",
    ),
    path(
        r"data/strip<int:number>.n3",
        jeremyday.theweeklystrip.rdf_views.strip_rdf,
        {"format": "n3"},
        name="tws_strip_rdf",
    ),
    path(
        r"data/strip<int:number>.xml",
        jeremyday.theweeklystrip.rdf_views.strip_rdf,
        {"format": "xml"},
        name="tws_strip_rdf",
    ),
]
