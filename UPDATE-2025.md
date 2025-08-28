# Update 2025

2025-08-25


## Rename master to main

Initiated on GitHub

    git branch -m master main
    git fetch origin
    git branch -u origin/main main
    git remote set-head origin -a

## Initialize Poetry

- Create scratch project
- Update from `jeremyday/settings.py`
- Update/replace URLconfs

## NEXT:  Create fresh `jeremydaysite` package for Django 5.2


Check static files for character encoding – seems they need an explicit charset decl now

TWSLib – may be need changes for changes to template API

## To do


Change email address to cleanskies@yahoo.co.uk

Delete references to Twitter. Add links to Threads and Instagram


Can we add an instagram feed without excessive tracking cookies (ha)

Replace use of `httplib2` with `requests` & `requests-cache`

Use of Beautifulsoup and html5lib needs review.
