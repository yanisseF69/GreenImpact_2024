''' This file contains the models for the database tables. '''
from django.db import models

# Create your models here.

class Categorie(models.Model):
    '''
    This class is used to create the model for the Categorie table in the database.
    '''

    nom_categorie = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return str(self.nom_categorie)

class Question(models.Model):
    '''
    This class is used to create the model for the Question table in the database.
    '''
    titre = models.CharField(max_length=100)

    categorie = models.ForeignKey(Categorie, related_name="question", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.titre)

class Option(models.Model):
    '''
    This class is used to create the model for the Option table in the database.
    '''
    question = models.ForeignKey(Question, related_name="reponse", on_delete=models.CASCADE)

    texte_option = models.CharField(max_length=25)
    valeur_carbone = models.FloatField()
    