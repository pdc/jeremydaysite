
from httplib2 import Http
from BeautifulSoup import BeautifulSoup, Tag
from django.core.cache import cache
from django.conf import settings
from datetime import datetime
import re

_http = None
def get_http():
    global _http
    if _http is None:
        _http = Http(settings.HTTPLIB2_CACHE_DIR)
    return _http

def entries_from_livejournal_url(url):
    """Given the URL of a front page of a LiveJournal journal, return a list of entries."""
    html_key = 'livejournal-%s' % url
    html = cache.get(html_key)
    if html is None:
        response, html = get_http().request(url, headers={'user-agent': 'jeremyday.uk/1.0 (like Godzilla; pdc@alleged.org.uk)'})
        cache.set(html_key, html)

    entries = entries_from_livejournal_html(html)
    return entries

def entries_from_livejournal_html(html):
    """Given HTML from a LiveJournal page, return a list of entries."""
    return list(entries_from_livejournal_html_iter(html))


# 11th Mar, 2010 at 8:35 AM
date_re = re.compile(r"""
    ^
    (?P<day>[0-9]{1,2}) (?:st|nd|rd|th) \s
    (?P<mon>[A-Z][a-z][a-z]) , \s
    (?P<year>[0-9]{4}) \s at \s
    (?P<hour>[0-9]{1,2}) :
    (?P<minute>[0-9]{2}) \s
    (?P<ampm>AM|PM)
    $
    """, re.VERBOSE)
mumfs = ['Zro', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def entries_from_livejournal_html_iter(html):
    """Given HTML from a LiveJournal page, generate a list of entries."""
    entry_sep_re = re.compile(r'<div id="asset-cleanskies-[0-9]+" class="post-asset asset">')
    html = html.replace('"height="', '" height="')
    #frags = entry_sep_re.split(html)
    soup = BeautifulSoup(html)

    for entry_soup in soup.findAll('div', 'post-asset asset'):
        heading_soup = entry_soup.find('h2')
        if heading_soup.find('span', 'lj-entry-securityicon'):
            continue
        link = heading_soup.a
        if link.string == 'moments between posts':
            continue
        entry = {
            'title': link.string,
            'href': link['href'],
        }

        date_str = entry_soup.find('abbr','datetime').string
        # strptime is helpless in the presence of ordinal suffixes.
        m = date_re.match(date_str)
        entry['published'] = datetime(
            int(m.group('year'), 10),
            mumfs.index(m.group('mon')),
            int(m.group('day'), 10),
            int(m.group('hour'), 10) % 12 + (12 if m.group('ampm') == 'PM' else 0),
            int(m.group('minute'), 10),
            0
        )

        body = entry_soup.find('div', 'asset-body')
        img_soup = entry_soup.find('div', 'user-icon').img
        if img_soup:
            entry['userpic'] = {
                'src': img_soup['src'],
                'width': int(img_soup['width'], 10),
                'height': int(img_soup['height'], 10),
                'title': img_soup['alt'],
            }
        img_soup.parent.extract()
        entry['content'] = str(body)

        for comment_soup in entry_soup.find('li', 'asset-meta-comments item asset-meta-no-comments'):
            s = comment_soup.string
            if s.endswith(' worms'):
                entry['comment_count'] = int(s[:-5], 10)
                break
        else:
            entry['comment_count'] = 0

        yield entry