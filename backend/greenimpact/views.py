''' This file contains the views for the GreenImpact app. '''

from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render


# Create your views here.

def start(request):
    '''
    This function is used to get the first 8 questions to display on the start page.
    '''

    ids = [ ]
    questions = [ ]

    print("requete start")
    print(request)
    while len(ids) < 8:

        with connection.cursor() as cursor:
            query = '''SELECT id_typage, nom_typage, id_categ
                        FROM greenimpact_typage
                        ORDER BY RANDOM() LIMIT 1'''

            cursor.execute(query)
            row = cursor.fetchone()
            if row[0] not in ids:
                ids.append(row[0])
                query = '''SELECT texte_question, type_question
                           FROM greenimpact_question 
                           WHERE id_typ = %s'''
                cursor.execute(query, [row[0]])
                quest = cursor.fetchone()
                query = '''SELECT nom_categorie
                           FROM greenimpact_categorie 
                           WHERE id_categorie = %s'''
                cursor.execute(query, [row[2]])
                categorie = cursor.fetchone()
                query = '''SELECT texte_option, empreinte_carbonne, id_option
                            FROM greenimpact_option
                            WHERE id_typ = %s;'''
                cursor.execute(query, [row[0]])
                options = cursor.fetchall()
                choix = [ ]
                for option in options:
                    reponse = {
                        "id" : option[2],
                        "nom" : option[0],
                        "valeur" : option[1],
                    }
                    choix.append(reponse)
                question = {
                    "titre" : quest[0],
                    "categorie" : categorie[0],
                    "type" : row[1],
                    "choix" : choix,
                    "unique" : quest[1] == 1,
                }
                questions.append(question)


    return render(request, 'radioQuestion.html', {'questions': questions})


def accueil(request):

    return render(request, 'index.html')


def result(request):
    '''
    This function is use to submit the answers and compute the final result.
    '''

    print("requete result")
    print(request)
    data = { }

    return JsonResponse(data)
