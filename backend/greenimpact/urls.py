''' This file is used to define the URL patterns for the Green Impact app. '''
from django.urls import path

from . import views

urlpatterns = [
    path("start/", views.start, name="start"),
    path("", views.index, name="index"),
    path('result/', views.result, name='result'),
    path('get_category_avg_carbon_footprint/',
         views.get_category_avg_carbon_footprint, name='get_category_avg_carbon_footprint'),
    ]
