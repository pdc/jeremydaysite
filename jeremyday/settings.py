# Django settings for jeremyday project.

import sys

import environ

env = environ.Env(
    DEBUG=(bool, False),
    STATIC_ROOT=(str, None),
    STATIC_URL=(str, None),
    SECRET_KEY=str,
    HTTPLIB2_CACHE_DIR=(str, '/var/tmp/jeremydaysite-httplib2-cache'),
)
environ.Env.read_env()
expand_path = environ.Path(__file__) - 2


DEBUG = env('DEBUG')
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = [
    'localhost',
    'jeremyday.org.uk',
    'jeremyday.uk',
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
SECRET_KEY = 'secret-key-value' if DEBUG else env('SECRET_KEY')

STATICFILES_DIRS = (
    expand_path('static'),
)

if env('STATIC_ROOT'):
    STATIC_URL = env('STATIC_URL', default='//static.jeremyday.uk/')
    STATIC_ROOT = env('STATIC_ROOT')  # e.g., '/home/alleged/static')
    if not DEBUG:
        STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
else:
    STATIC_URL = '/STATIC/'

FRONTPAGE_DIR = expand_path('content')
LIVEJOURNAL_URL = 'https://cleanskies.livejournal.com/'
LIVEJOURNAL_ATOM_URL = 'https://cleanskies.livejournal.com/data/atom'
HTTPLIB2_CACHE_DIR = env('HTTPLIB2_CACHE_DIR')
TWS_FILE = expand_path('content/tws.data')
TWS_SRC_PREFIX = STATIC_URL
TWS_IMAGE_DIR = expand_path('static')
TWS_FEED_PER_PAGE = 20

SPREADLINKS_DIR = expand_path('linklibraries')
SPREADLINKS_PER_PAGE = 20


MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'jeremyday.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            expand_path('tpl'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                "jeremyday.context_processors.settings",
                "jeremyday.context_processors.is_css_naked",
            ]
        },
    },
]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    'spreadlinks',
    'jeremyday.theweeklystrip',
    'jeremyday.frontpage',
)
