# Encoding: UTF-8

from urllib import urlencode
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.conf import settings
from jeremyday import twslib
from datetime import datetime, date
import time

def render_with_template(default_template_name, default_base_template_name='base.html', mimetype='text/html'):
    """Decorator to wrap template-based rendering around a view function returning template variables."""
    def decorator(func):
        def wrapped_handler(request, template_name=None, base_template_name=None, *args, **kwargs):
            result = func(request, *args, **kwargs)
            if isinstance(result, HttpResponse):
                return result
            if not result.get('base_template_name'):
                result['base_template_name'] = base_template_name or default_base_template_name
            return render_to_response(template_name or default_template_name, result, RequestContext(request), mimetype=mimetype)
        return wrapped_handler
    return decorator

@render_with_template('jeremyday/tws-strip.html')
def latest(request):
    strips = twslib.get_tws(settings.TWS_FILE, settings.TWS_SRC_PREFIX);
    return all_about_the_nth_strip(request, strips, -1)

@render_with_template('jeremyday/tws-strip.html')
def strip_page(request, number):
    ordinal = int(number)

    strips = twslib.get_tws(settings.TWS_FILE, settings.TWS_SRC_PREFIX);
    if ordinal < 1:
        # Or would a 404 be more appropriate?
        return HttpResponseRedirect(reverse('tws_strip', kwargs={number: '1'}))
    if ordinal > len(strips):
        return HttpResponseRedirect(reverse('tws_strip', kwargs={number: str(len(strips))}))

    indexes_by_number = dict((strip['number'], i) for (i, strip) in enumerate(strips))
    index = indexes_by_number[ordinal]

    return all_about_the_nth_strip(request, strips, index)

def all_about_the_nth_strip(request, strips, index):
    if index < 0:
        index += len(strips)
    strip = strips[index]
    prev = strips[index - 1] if 0 < index else None
    next = strips[index + 1] if index + 1 < len(strips) else None
    jumps = give_me_jumps(strips, strip)

    twitter_share_params = [
        ('url', request.build_absolute_uri(reverse('tws_strip',kwargs={'number': '%d' % strip['number']}))),
        ('via', 'cleanskies'),
        ('text', u'Jeremy Day’s The Weekly Strip {0} ‘{1}’'
            .format(strip['number'], strip['title'])
            .encode('UTF-8')),
        ('lang', 'en'),
    ]
    twitter_share_url = 'https://twitter.com/share?{0}'.format(
        urlencode(twitter_share_params).replace('+', '%20'))

    return {
        'tws': strips,
        'strip': strip,
        'prev': prev,
        'next': next,
        'first': strips[0],
        'last': strips[-1],
        'jumps': jumps,
        'twitter_share_url': twitter_share_url,
    }

def give_me_jumps(strips, strip=None):
    jumps = []
    prev_year = 0
    for other_strip in strips:
        year = other_strip['date'].year
        if year > prev_year:
            href = reverse('tws_year', kwargs={'year': str(year)})
            jumps.append((str(year), other_strip, href, True))
            prev_year = year
    href = reverse('tws_strip', kwargs={'number': str(strips[-1]['number'])})
    jumps.append(('Latest', strips[-1], href, strip != strips[-1]))
    return jumps

@render_with_template('jeremyday/tws-year.html')
def year_page(request, year):
    year = int(year)

    strips = twslib.get_tws(settings.TWS_FILE, settings.TWS_SRC_PREFIX)
    # Binary chop to find first strip for this year.
    lo, hi = 0, len(strips) # Invariant: strips[:lo] < year and year <= strips[hi:]
    while lo < hi:
        m = (lo + hi) // 2
        if strips[m]['date'].year < year:
            lo = m + 1
        else:
            hi = m
    beg = lo

    # ditto to find upper bound.
    hi = len(strips) # New invariant: strips[:lo] <= year and year < strips[hi:]
    while lo < hi:
        m = (lo + hi) // 2
        if strips[m]['date'].year > year:
            hi = m
        else:
            lo = m + 1
    end = hi

    months = ['Zeugmonth', 'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December']
    month_strips = []
    cur_m = None
    cur_strips = []
    for strip in strips[beg:end]:
        m = strip['date'].month
        if m != cur_m:
            if cur_m:
                month_strips.append((months[cur_m], cur_strips))
            cur_m = m
            cur_strips = [strip]
        else:
            cur_strips.append(strip)
    if cur_m:
        month_strips.append((months[cur_m], cur_strips))

    jumps = give_me_jumps(strips)

    return {
        'month_strips': month_strips,
        'year': year,
        'prev_year': year - 1 if beg > 0 else None,
        'next_year': year + 1 if end < len(strips) else None,
        'jumps': jumps,
    }

def by_date(request, year, month, day):
    """Mostly intended for doing redirects from the old site, which was organized by date not number."""
    d = date(int(year), int(month, 10), int(day, 10))
    strips = twslib.get_tws(settings.TWS_FILE, settings.TWS_SRC_PREFIX)

    # Binary chop (again!) to find first strip following this date.
    lo, hi = 0, len(strips) # Invariant: strips[:lo] < d and d <= strips[hi:]
    while lo < hi:
        m = (lo + hi) // 2
        if strips[m]['date'] < d:
            lo = m + 1
        else:
            hi = m

    if hi < len(strips):
        return HttpResponseRedirect(reverse('tws_strip', kwargs={'number': strips[hi]['number']}))
    raise Http404


@render_with_template('jeremyday/tws.atom', mimetype='application/atom+xml')
def reading_order_feed(request, page=None):
    """Returns a feed in reading order, as a 'paged feed' (see RFC 5005 for what this means).

    TWS entries have a date that is the date the strip was drawn,
    and may differ from the date it was added to the site.
    This feed is in strip’s date order. This means that strips inserted in to the
    backstory will not appear in the latest-entries page.

    latest (page 1) is the most recent N entries (according to the strip dates).
    page 2 is the next most recent N entries
    and so on.
    """
    strips = twslib.get_tws(settings.TWS_FILE, settings.TWS_SRC_PREFIX)
    per_page = settings.TWS_FEED_PER_PAGE
    max_page = (len(strips) + per_page - 1) // per_page
    if page:
        page = int(page)
    else:
        page = 1

    # Pages count backwards from the end.
    end = len(strips) - (page - 1) * per_page # Page 1 ends with the last strip.
    beg = end - per_page if end > per_page else 0

    # Reverse chronooogical order means the NEXT page is OLDER strips and LAST is OLDEST strips. Right?
    first_href = reverse('tws_reading_order_feed')
    last_href = reverse('tws_reading_order_feed', kwargs={'page': str(max_page)})
    self_href = (first_href if page == 1
        else last_href if page == max_page
        else reverse('tws_reading_order_feed', kwargs={'page': str(page)}))
    next_href = (None if page == max_page
        else reverse('tws_reading_order_feed', kwargs={'page': str(page + 1)}))
    prev_href = (None if page == 1
        else first_href if page == 2
        else reverse('tws_reading_order_feed', kwargs={'page': str(page - 1)}))

    self_href = self_href

    subset = strips[beg:end]
    subset.reverse()
    twslib.add_mtimes(subset, settings.TWS_IMAGE_DIR)
    feed_updated = 0
    for strip in subset:
        strip['icon_src'] = request.build_absolute_uri(strip['icon_src'])
        strip['image_src'] = request.build_absolute_uri(strip['image_src'])
        strip['page_href'] = request.build_absolute_uri(reverse('tws_strip', kwargs={'number': str(strip['number'])}))
        strip['id'] = 'tag:jeremyday.org.uk,2010:tws-strip:%d' % strip['number']
        updated = time.strftime('%Y-%m-%dT%H:%M:%S%z',time.localtime(strip['mtime']))
        updated = '%s:%s' % (updated[:-2], updated[-2:]) # RFC 3339 required +00:00 not +0000
        strip['updated'] = updated

        if updated > feed_updated: # This is the first time I have actually exploited the sortability of RFC 3339 datetimes!
            feed_updated = updated

    tpl_args = {
        'title': 'The Weekly Strip by Jeremy Day (in reading order)',
        'id': 'tag:jeremyday.org.uk,2010:tws-in-reading-order',
        'page': page,
        'home': request.build_absolute_uri(reverse('tws_latest')),
        'self': request.build_absolute_uri(self_href),
        'first': request.build_absolute_uri(first_href),
        'last': request.build_absolute_uri(last_href),
        'prev': prev_href and request.build_absolute_uri(prev_href),
        'next': next_href and request.build_absolute_uri(next_href),
        'updated': feed_updated,
        'strips': subset,
    }
    return tpl_args

