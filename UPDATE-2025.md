# Update 2025

2025-08-25

2a01:4f8:c013:4422::/64
188.245.56.86

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

- Update `data.numbers` to to latest Numbers
- Replace `http:` with `https:` in `data.csv`
- Add links to Means of Production
- Add images for images that are now missing
- Update Spreadlinks project and publish to PyPI


## Deployment

I tried creating cache directories in `/var/cache` but Django raised an exception
complaining about its being a read-only file system (I guess because of
`ProtectSystem:strict` in the Systemd unit?). I created cache directories in
`/hoome/jeremyday` and it works, so I will leave it at that for now.

Seems that around 2015 we started changing to domain name `jeremyday.uk`.
I have updated most of the site and its configuration to use the new domain name,
and created redirects from the old domain name.

## Edits

Change email address to cleanskies@yahoo.co.uk

## To do



Delete references to Twitter. Add links to Threads and Instagram

Hide pagination on projects page when no second page



TWSLib – may be need changes for changes to template API (the static generation might be
broken but I do not think it is in use)

Check static files for character encoding – seems they need an explicit charset decl now



Strange Machine – all the images have been made unavailable by Flickr, might just need URLs adjusted?


Can we add an instagram feed without excessive tracking cookies (ha)

Replace use of `httplib2` with `requests` & `requests-cache`

Use of Beautifulsoup and html5lib needs review.

Change CSS Naked Day to use new date 9 April
