''' This file is used to define the URL patterns for the Green Impact app. '''
from django.urls import path

from . import views

urlpatterns = [
    path("start/", views.start, name="start"),
    path("", views.index, name="index"),
    ]
