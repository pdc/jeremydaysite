# Create your views here.

from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.conf import settings
from jeremyday import twslib

def render_with_template(default_template_name, default_base_template_name='base.html'):
    """Decorator to wrap template-based rendering around a view function returning template variables."""
    def decorator(func):
        def wrapped_handler(request, template_name=None, base_template_name=None, *args, **kwargs):
            result = func(request, *args, **kwargs)
            if isinstance(result, HttpResponse):
                return result
            if not result.get('base_template_name'):
                result['base_template_name'] = base_template_name or default_base_template_name
            return render_to_response(template_name or default_template_name, result, RequestContext(request))
        return wrapped_handler
    return decorator
    
@render_with_template('jeremyday/tws-strip.html')
def latest(request):
    strips = twslib.get_tws(settings.TWS_FILE, settings.TWS_SRC_PREFIX);
    return all_about_the_nth_strip(strips, -1) 
    
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
    
    return all_about_the_nth_strip(strips, index)
    
def all_about_the_nth_strip(strips, index):
    if index < 0:
        index += len(strips)
    strip = strips[index]
    prev = strips[index - 1] if 0 < index else None
    next = strips[index + 1] if index + 1 < len(strips) else None
    
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
    
    return {
        'tws': strips,
        'strip': strip,
        'prev': prev,
        'next': next,
        'jumps': jumps,
    }
    
    
@render_with_template('jeremyday/tws-year.html')
def year_page(request, year):
    year = int(year)
    
    strips = twslib.get_tws(settings.TWS_FILE, settings.TWS_SRC_PREFIX);
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
    
    months = ['Zeugmonth', 'January', 'Feburary', 'March', 'April', 'May', 'June',
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
    
    
    return {
        'month_strips': month_strips,
        'year': year,
        'prev_year': year - 1 if beg > 0 else None,
        'next_year': year + 1 if end < len(strips) else None
    }