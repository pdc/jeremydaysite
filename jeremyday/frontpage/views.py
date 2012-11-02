# Create your views here.

from django.http import HttpResponse, Http404
from django.template import RequestContext, loader, Context
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.conf import settings
import os
import codecs
import httplib2
import json
from xml.etree import ElementTree as ET
from jeremyday import twslib
from jeremyday.livejournal import entries_from_livejournal_url

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

LIVEJOURNAL_ATOM_CACHE_KEY = 'livejournal-atom-%s-1' % settings.LIVEJOURNAL_ATOM_URL
LIVEJOURNAL_HTML_CACHE_KEY = 'livejournal-rendered-%s-' % settings.LIVEJOURNAL_URL
def livejournal(request):
    html = cache.get(LIVEJOURNAL_HTML_CACHE_KEY)

    if not html:
        feed = entries_from_livejournal_url(settings.LIVEJOURNAL_URL)

        if False and not feed:
            # For some reason I could not find the Atom formatted feed before now.
            body = cache.get(LIVEJOURNAL_ATOM_CACHE_KEY)
            if not body:
                url = 'http://cleanskies.livejournal.com/data/atom'
                http = httplib2.Http(settings.HTTPLIB2_CACHE_DIR)
                livejournal_response, body = http.request(url, 'GET', headers={'User-Agent': 'jeremyday.org.uk/1.0 (pdc@alleged.org.uk)'})
                cache.set(LIVEJOURNAL_ATOM_CACHE_KEY, body)
            feed_elt = ET.XML(body)
            for entry_elt in feed_elt:
                entry = {}
                for item_elt in entry_elt:
                    if item_elt.tag == '{http://www.w3.org/2005/Atom}link' and item_elt.get('rel') == 'alternate':
                        entry['href'] = item_elt.text
                    elif item_elt.tag == '{http://www.w3.org/2005/Atom}title':
                        entry['title'] = item_elt.text
                    elif item_elt.tag == '{http://www.w3.org/2005/Atom}content':
                        entry['content'] = item_elt.text
                feed.append(entry)

        if feed:
            template = loader.get_template('jeremyday/livejournal.div.html')
            context = Context({'feed': feed})
            html = template.render(context)
            cache.set(LIVEJOURNAL_HTML_CACHE_KEY, html)

    result = {
        'success': True,
        'body': html,
    }
    response = HttpResponse(json.dumps(result, 'UTF-8'), mimetype='text/javascript')
    return response