# Create your views here.

from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.conf import settings
import os
import codecs
from jeremyday import twslib
import httplib2
from BeautifulSoup import BeautifulSoup, Tag
import json

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

@render_with_template('jeremyday/front.html')
def front_page(request):
    text_file = os.path.join(settings.FRONTPAGE_DIR,'introduction.md')
    text = codecs.open(text_file, 'r', 'UTF-8').read()
    tws = twslib.get_tws(settings.TWS_FILE, settings.TWS_SRC_PREFIX)
    
    other_sites = twslib.get_sites(os.path.join(settings.FRONTPAGE_DIR, 'other-sites.data'))
    return {
        'text': text,
        'tws': reversed(tws[-12:]),
        'other_sites': other_sites,
    }

LIVEJOURNAL_CACHE_KEY = 'jeremyday-livejournal'
def livejournal(request):
    html = cache.get(LIVEJOURNAL_CACHE_KEY)
    if not html:
        url = 'http://www.livejournal.com/customview.cgi?username=cleanskies&amp;styleid=101'
        http = httplib2.Http('/tmp/httplib2')
        livejournal_response, body = http.request(url, 'GET')
        soup = BeautifulSoup(body)
        posts = soup.findAll('div', 'post-asset asset')
        div = Tag(soup, 'div')
        for i, post in enumerate(posts):
            heading = post.find('h2')
            if heading.find('a', text='moments between posts'):
                continue
            heading.name = 'h3'
            div.insert(i, post)
        html = unicode(div)
        cache.set(LIVEJOURNAL_CACHE_KEY, html)
    result = {
        'success': True,
        'body': html,
    }
    response = HttpResponse(json.dumps(result, 'UTF-8'), mimetype='text/javascript')
    return response
    