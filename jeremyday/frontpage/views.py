# Create your views here.

from pathlib import Path
from xml.etree import ElementTree as ET

import httplib2
from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.template import loader
from django.template.response import TemplateResponse
from django.utils import safestring
from markdown import Markdown

from jeremyday import twslib
from jeremyday.livejournal import entries_from_livejournal_url
from jeremyday.other_sites import get_sites

formatter = Markdown()

frontpage_dir = Path(settings.FRONTPAGE_DIR)


def front_page(request):
    text_file = frontpage_dir / "introduction.md"
    with open(text_file, "r", encoding="UTF-8") as input:
        text = input.read()
    tws = twslib.get_tws(settings.TWS_FILE, settings.TWS_SRC_PREFIX)

    other_sites = get_sites(frontpage_dir / "other-sites.yaml")
    return TemplateResponse(
        request,
        "jeremyday/front.html",
        {
            "text": text,
            "text_formatted": safestring.mark_safe(formatter.convert(text)),
            "tws": reversed(tws[-12:]),
            "other_sites": other_sites,
        },
    )


LIVEJOURNAL_ATOM_CACHE_KEY = "livejournal-atom-%s-1" % settings.LIVEJOURNAL_ATOM_URL
LIVEJOURNAL_HTML_CACHE_KEY = "livejournal-rendered-%s-" % settings.LIVEJOURNAL_URL


def livejournal(request):
    html = cache.get(LIVEJOURNAL_HTML_CACHE_KEY)

    if not html:
        feed = entries_from_livejournal_url(settings.LIVEJOURNAL_URL)

        if False and not feed:
            # For some reason I could not find the Atom formatted feed before now.
            body = cache.get(LIVEJOURNAL_ATOM_CACHE_KEY)
            if not body:
                url = "http://cleanskies.livejournal.com/data/atom"
                http = httplib2.Http(settings.HTTPLIB2_CACHE_DIR)
                livejournal_response, body = http.request(
                    url,
                    "GET",
                    headers={"User-Agent": "jeremyday.uk/1.0 (pdc@alleged.org.uk)"},
                )
                cache.set(LIVEJOURNAL_ATOM_CACHE_KEY, body)
            feed_elt = ET.XML(body)
            for entry_elt in feed_elt:
                entry = {}
                for item_elt in entry_elt:
                    if (
                        item_elt.tag == "{http://www.w3.org/2005/Atom}link"
                        and item_elt.get("rel") == "alternate"
                    ):
                        entry["href"] = item_elt.text
                    elif item_elt.tag == "{http://www.w3.org/2005/Atom}title":
                        entry["title"] = item_elt.text
                    elif item_elt.tag == "{http://www.w3.org/2005/Atom}content":
                        entry["content"] = item_elt.text
                feed.append(entry)

        if feed:
            template = loader.get_template("jeremyday/livejournal.div.html")
            html = template.render({"feed": feed}, request)
            cache.set(LIVEJOURNAL_HTML_CACHE_KEY, html)

    result = {
        "success": True,
        "body": html,
    }
    response = JsonResponse(result, json_dumps_params={"indent": 4})
    return response
