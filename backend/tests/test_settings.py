""" Settings for running tests. """
from django.conf import settings

MIDDLEWARE = settings.MIDDLEWARE

ROOT_URLCONF = 'backend.urls'

TEMPLATES = settings.TEMPLATES

TEST = {'NAME': 'test_database'}

# Test database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mif10',
        'USER': "admin",
        'PASSWORD': "admin",
        'HOST': '192.168.75.19',
        'PORT': '',
    },
    'test': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test_mif10',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': '192.168.75.19',
        'PORT': '',
        'MIGRATE': False,
    }
}

MIGRATION_MODULES = {
    'greenimpact': 'greenimpact.test_migrations',
}


# Test runner
TEST_RUNNER = 'tests.test_runner.ManagedModelTestRunner'

# Test client settings
TEST_REQUEST_DEFAULT_FORMAT = 'json'
TEST_NON_SERIALIZED_APPS = []
