# Jeremy Day site

This is the source code for the web site <https://jeremyday.org.uk>.

Unless you are me (or Jeremy Day) you probably do not want to use this project
verbatim, but might steal some ideas for a similar site for someone else?

## Deployment

Assuming a very conventional Nginx → Gunicorn setup on a system using Systemd,
it might be set up like the following. (This assumes it sis being installed in to
a generic Debian GNU/Linux box.)

Create system user `jeremyday` and directory `/home/jeremyday` with subdirs
`sites`, `etc`. Start the environment file. This will be referenced in the
`EnvironmentFile` key of the Systemd unit for Gunicorn.

    mkdir /home/jeremyday/{sites,etc}
    ENV=/home/jeremyday/etc/production.env
    echo SECRET_KEY=$(pwgen 50) >> $ENV
    echo ALLOWED_HOSTS=jeremyday.org.uk,jeremyday.uk,next.jeremyday.org.uk >> $ENV

Unpack the site in to the sites folder

    cd /home/jeremyday/sites
    git clone https://github.com/pdc/jeremyday.git

Create appropriate static server definitions in Nginx and link to static directories
from where static files are served:

    ln -s /home/jeremyday/sites/jeremyday/1999 /var/www/jeremyday.lastcentury
    ln -s /home/jeremyday/sites/jeremyday/noughties /var/www/jeremyday.noughties

These are the static sites <https://lastcentury.jeremyday.org.uk> and <https://noughties.jeremyday.org.uk>.

Create directories for caching downloads & Django objects:

    HTTPLIB2_CACHE_DIR=/var/cache/jeremyday/requests
    CACHE_DIR=/var/cache/jeremyday/django
    mkdir $HTTPLIB2_CACHE_DIR $CACHE_DIR
    chown jeremyday.jeremyday $HTTPLIB2_CACHE_DIR $CACHE_DIR
    echo HTTPLIB2_CACHE_DIR=$HTTPLIB2_CACHE_DIR >> $ENV
    echo CACHE_URL=filecache://$CACHE_DIR >> $ENV

What next? Oh yes, the virtual environment.

    python3 -mvenv /home/jeremyday/venv
    source /home/jeremyday/venv/bin/activate
    cd /home/jeremyday/sites/jeremyday
    poetry install
    pip install gunicorn

Remember to use the environment file while testing & running management commands.

    cd /home/jeremyday/sites/jeremyday
    env $(cat $ENV) ./manage.py check
    echo STATIC_DIR=/home/jeremyday/static >> $ENV
    echo STATIC_ROOT=https://static.jeremyday.org.uk/ >> $ENV
    env $(cat $ENV) ./manage.py collectstatic

Test Gunicorn:

    cd /home/jeremyday/sites/jeremyday
    env $(cat $ENV) /home/jeremyday/venv/bin/gunicorn jeremydaysite.wsgi
