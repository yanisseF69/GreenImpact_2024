from django.db import models

# Create your models here.

class Categorie(models.Model):

    nom_categorie = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return self.nom_categorie

class Question(models.Model):

    titre = models.CharField(max_length=100)

    categorie = models.ForeignKey(Categorie, related_name="question", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.titre

class Option(models.Model):

    question = models.ForeignKey(Question, related_name="reponse", on_delete=models.CASCADE)

    texte_option = models.CharField(max_length=25)
    
    valeur_carbone = models.FloatField()


