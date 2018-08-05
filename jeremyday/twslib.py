#!/usr/bin/env python
# encoding: utf-8
"""
make-index.py

Created by Damian Cugley on 2008-11-09.
Copyright © 2008 Damian Cugley. All rights reserved.
"""

import os
import sys
import markdown
import getopt
import codecs
import datetime
import time
from django.core.cache import cache


def word_iter(s):
    """Split line in to words in a fashion like shlex.split, but simpler."""
    quote = None  # Quote character being matched, or None
    beg = None  # First char of word being scanned, or None
    for pos, c in enumerate(s):
        if quote and c == quote:
            # end of quoted string
            yield s[beg:pos]
            beg = quote = None
        elif quote:
            pass
        elif c == '"':
            # Start of quoted string
            if beg is not None:
                yield s[beg:pos]
            beg = pos + 1
            quote = c
        elif c == '#':
            break
        elif c.isspace():
            if beg is not None:
                yield s[beg:pos]
            beg = None
        elif beg is None:
                beg = pos
    if quote:
        raise FormatException('Expected closing quotation mark.')
    if beg:
        yield s[beg:]


def tws_iter(in_file, prefix):
    """Load the list of strips from tws.data."""
    with open(in_file, 'r', encoding='UTF-8') as input:
        count = 0
        for line in input:
            line = line.strip()
            if line:
                count += 1
                xs = list(word_iter(line))
                d = dict(zip(['image_src', 'icon_src', 'title', 'lj'], xs))
                s = d['image_src'].replace('-', '')[:8]
                d['page_href'] = '%s/%s.html' % (s[:4], s)
                date = datetime.date(int(s[:4]), int(s[4:6], 10), int(s[6:8], 10))
                d['date'] = date
                d['number'] = count
                d['image_src_sans_prefix'] = '%s/%s' % (s[:4], d['image_src'])
                d['image_src'] = '%s%s/%s' % (prefix, s[:4], d['image_src'])
                d['icon_src'] = '%s%s/%s' % (prefix, s[:4], d['icon_src'])
                yield d
    print('Read', count, 'entries from', in_file)


TWS_CACHE_KEY = 'tws-data'
TWS_WHEN_CACHE_KEY = 'tws-data-when'


def get_tws(in_file, prefix):
    result = None
    when_cached = cache.get(TWS_WHEN_CACHE_KEY)
    if when_cached:
        mtime = os.stat(in_file).st_mtime
        if mtime < when_cached:
            result = cache.get(TWS_CACHE_KEY)
    if result is None:
        result = list(tws_iter(in_file, prefix))
        result.sort(key=lambda d: d['date'])
        cache.set(TWS_CACHE_KEY, result)
        cache.set(TWS_WHEN_CACHE_KEY, time.time())
    return result


def add_mtimes(strips, image_dir):
    for strip in strips:
        if 'mtime' not in strip:
            image_file = os.path.join(image_dir, strip['image_src_sans_prefix'])
            mtime = os.stat(image_file).st_mtime
            strip['mtime'] = mtime
    return strips


def sites_iter(in_file):
    """Load the list of other web sites."""
    with open(in_file, 'r', encoding='UTF-8') as input:
        count = 0
        for line in input:
            line = line.strip()
            if line:
                count += 1
                xs = list(word_iter(line))
                if xs:
                    d = dict(zip(['href', 'title', 'icon_src'], xs))
                    d['number'] = count
                    yield d
    print('Read', count, 'entries from', in_file)


cached_sites = None


def get_sites(in_file):
    global cached_sites
    if cached_sites is None:
        cached_sites = list(sites_iter(in_file))
        # cached_sites.sort(key=lambda d: d['date'])
    return cached_sites


def make_index(template_name='index.html', template_paths=['templates'], out_dir='out', out_name='index.html', is_verbose=True):
    loader = TemplateLoader(template_paths)
    print('Default_encoding:', loader.default_encoding)
    template = loader.load(template_name)

    with open('index-content.markdown', 'r', encoding='UTF-8') as input:
        content_markdown = input.read()
    content_html = markdown.markdown(content_markdown)
    tws = get_tws()
    sites = get_sites()
    stream = template.generate(tws=tws, sites=sites, content=Markup(content_html))

    output = open(os.path.join(out_dir, out_name), 'w')
    stream.render(method='html', out=output, encoding='utf-8')
    if is_verbose: print('Wrote HTML to', out_name)


help_message = '''
The help message goes here.
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
  if argv is None:
    argv = sys.argv
  try:
    try:
      opts, args = getopt.getopt(argv[1:], "ho:v", ["help", "output="])
    except getopt.error as msg:
      raise Usage(msg)

    # option processing
    for option, value in opts:
      if option == "-v":
        verbose = True
      if option in ("-h", "--help"):
        raise Usage(help_message)
      if option in ("-o", "--output"):
        output = value

    make_index()

  except Usage as err:
    print(sys.argv[0].split("/")[-1] + ": " + str(err.msg), file=sys.stderr)
    print("\t for help use --help", file=sys.stderr)
    return 2


if __name__ == "__main__":
  sys.exit(main())
