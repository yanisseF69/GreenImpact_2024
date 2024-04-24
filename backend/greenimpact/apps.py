'''This file is used to configure the app name for the Green Impact app.'''
from django.apps import AppConfig

class GreenimpactConfig(AppConfig):
    '''
    This class is used to configure the app name for the Green Impact app.
    '''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'greenimpact'
