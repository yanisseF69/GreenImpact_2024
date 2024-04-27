""" Settings for running tests. """
from django.conf import settings
from django.test import override_settings

MIDDLEWARE = settings.MIDDLEWARE

ROOT_URLCONF = 'backend.urls'

TEMPLATES = settings.TEMPLATES

TEST = {'NAME': 'test_database'}

# Test database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test_mif10',
        'USER': "admin",
        'PASSWORD': "admin",
        'HOST': '192.168.75.19',
        'PORT': '',
        'TEST': {
            'NAME': 'test_mif10',
        }
    }
}

# Test runner
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Test client settings
TEST_REQUEST_DEFAULT_FORMAT = 'json'
TEST_NON_SERIALIZED_APPS = []
