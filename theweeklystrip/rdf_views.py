from rdflib import ConjunctiveGraph
from rdflib import BNode, Literal, Namespace, RDF, URIRef
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.conf import settings
from jeremyday import twslib

DC = Namespace('http://purl.org/dc/elements/1.1/')
FOAF = Namespace('http://xmlns.com/foaf/0.1/')
ALLEGED = Namespace('http://www.alleged.org.uk/2010/comics/')
TWS = Namespace('http://jeremyday.org.uk/tws/r/')

def strip_conneg(request, number):
    options = {
        'text/html': ('tws_strip', {'number': number}),
        'application/rdf+xml': ('tws_strip_rdf', {'number': number, 'format': 'xml'}),
        'text/n3': ('tws_strip_rdf', {'number': number, 'format': 'n3'}),
    }
    accept_raw = request.META.get('HTTP_ACCEPT', 'text/html')
    best_media = None
    best_q = None
    for accept_clause in accept_raw.split(','):
        terms = accept_clause.split(';')
        media_range = terms.pop(0)
        params = dict((k.strip(), v.strip()) for (k,v) in ((kv.split('=', 1) for kv in terms)))
        q = float(params.get('q', '1'))
        if best_q is None or q > best_q:
            is_found = False
            for media in options.keys():
                if (media_range == '*/*'
                        or media_range.endswith('/*') and media.startswith(media_range[:-1])
                        or media_range == media):
                    best_q, best_media = q, media_range
                    break
    view_name, kwargs = options[best_media]
    return HttpResponseRedirect(reverse(view_name, kwargs=kwargs))
    
format_mimetypes = {
    'xml': 'application/rdf+xml',
    'n3': 'text/plain',
}
def strip_rdf(request, number, format):
    ordinal = int(number)
    if ordinal < 1:
        raise Http404
    strips = twslib.get_tws(settings.TWS_FILE, settings.TWS_SRC_PREFIX);
    if ordinal > len(strips):
        raise Http404
        
    # Strips are organized by date, not number.
    # So we need to work out which strips has this number.
    indexes_by_number = dict((strip['number'], i) for (i, strip) in enumerate(strips))
    index = indexes_by_number[ordinal]
    strip = strips[index]
    
    graph = ConjunctiveGraph()
    graph.bind('alleged', ALLEGED)
    graph.bind('dc', DC)
    graph.bind('foaf', FOAF)
    graph.bind('tws', TWS)
    
    strip_subject = TWS[number]
    graph.add((strip_subject, RDF.type, ALLEGED['comic']))
    graph.add((strip_subject, DC['creator'], Literal('Jeremy Day')))
    graph.add((strip_subject, DC['title'], Literal(strip['title'])))
    graph.add((strip_subject, DC['date'], Literal(strip['date'].isoformat())))
    
    graph.add((strip_subject, ALLEGED['excerpt'], URIRef(strip['icon_src'])))
    graph.add((strip_subject, ALLEGED['image'], URIRef(strip['image_src'])))
    
    if ordinal > 1:
        graph.add((strip_subject, ALLEGED['prev-page'], TWS[str(ordinal - 1)]))
    if ordinal < len(strips):
        graph.add((strip_subject, ALLEGED['next-page'], TWS[str(ordinal + 1)]))
    
    response = HttpResponse(graph.serialize(format=format),
        mimetype=format_mimetypes[format])
    return response
    
    
    