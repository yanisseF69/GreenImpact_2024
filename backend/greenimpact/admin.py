'''This file is used to register the models in the admin panel.'''
from django.contrib import admin
from .models import Categorie, Question, Option

# Register your models here.
admin.site.register(Categorie)
admin.site.register(Question)
admin.site.register(Option)
