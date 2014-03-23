# Django settings for jeremyday project.

import os, sys

root_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
def local_file(file_name):
    return os.path.join(root_dir, file_name)

submodules_dir = local_file('submodules')
if submodules_dir not in sys.path:
    sys.path.append(submodules_dir)


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = [
    'jeremyday.org.uk',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'dev.db',             # Or path to database file if using sqlite3.
        'USER': '',             # Not used with sqlite3.
        'PASSWORD': '',         # Not used with sqlite3.
        'HOST': '',             # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',             # Set to empty string for default. Not used with sqlite3.
    }
}

CACHE_BACKEND = 'locmem://' # TODO. Should I instead be using memcached?

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'
USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-GB'

SITE_ID = 2

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'w1oim%8yfl75mey03=m&^mmnk+$a^ddrlo%*wy^b0@10)in5#&'

STATICFILES_DIRS = (
    local_file('static'),
)

# Where static files are collected:
STATIC_ROOT = '/home/jeremyday/static'

# Where static files are served from:
STATIC_URL = 'http://static.jeremyday.org.uk/'

FRONTPAGE_DIR = local_file('content')
LIVEJOURNAL_URL = 'http://cleanskies.livejournal.com/'
LIVEJOURNAL_ATOM_URL = 'http://cleanskies.livejournal.com/data/atom'
HTTPLIB2_CACHE_DIR = '/home/jeremyday/caches/httplib2'
TWS_FILE = local_file('content/tws.data')
TWS_SRC_PREFIX = STATIC_URL
TWS_IMAGE_DIR = local_file('static')
TWS_FEED_PER_PAGE = 20

SPREADLINKS_DIR = local_file('linklibraries')
SPREADLINKS_PER_PAGE = 20

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "jeremyday.context_processors.is_css_naked",
]

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'jeremyday.urls'

TEMPLATE_DIRS = (
    local_file('tpl'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.markup',
    'django.contrib.staticfiles',

    'spreadsite.spreadlinks',
    'jeremyday.theweeklystrip',
    'jeremyday.frontpage',
)
