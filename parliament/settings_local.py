import os

DEBUG = True

PROJ_ROOT = os.path.dirname(os.path.realpath(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'parliament.sqlite',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
}

HANSARD_CACHE_DIR = os.path.join(PROJ_ROOT, 'hansard-cache')
SITE_URL='http://openparliament.ca'

# Currently unused
# RECAPTCHA_PUBLIC_KEY = '<your public key>'
# RECAPTCHA_PRIVATE_KEY = '<your private key>'

CACHE_BACKEND = 'dummy://'
CACHE_MIDDLEWARE_SECONDS = 60 * 60 * 3

# For search to work, you need to have a running instance of Apache Solr
# (If you just leave this as an invalid URL, the site will work with the
# exception of search features.)
HAYSTACK_SOLR_URL = 'http://127.0.0.1:8983/solr'
# If set to True, Solr will be sent an update command whenever new searchable
# data is added.
PARLIAMENT_AUTOUPDATE_SEARCH_INDEXES = False

TWITTER_USERNAME = ''
TWITTER_PASSWORD = ''
TWITTER_LIST_NAME = 'mps'

PARLIAMENT_WORDCLOUD_COMMAND = ('/usr/bin/java', '-jar' ,"/path/to/ibm-word-cloud.jar",  '-c', os.path.join(PROJ_ROOT, '..', 'config', 'wordcloud.conf'), '-w', '800')

PARLIAMENT_SEND_EMAIL = False

PARLIAMENT_HTV_API_KEY = '' # Key for the How'd They Vote API, howdtheyvote.ca

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'verysecretindeed'

