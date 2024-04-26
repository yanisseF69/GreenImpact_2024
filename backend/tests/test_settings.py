""" Settings for running tests. """
from django.conf import settings
from django.test import override_settings

MIDDLEWARE = settings.MIDDLEWARE

ROOT_URLCONF = 'backend.urls'

TEMPLATES = settings.TEMPLATES

TEST = {'NAME': 'test_database'}
