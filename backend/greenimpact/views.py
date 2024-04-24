''' This file contains the views for the GreenImpact app. '''
import random

from django.db import connection
from django.http import JsonResponse

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
            categorie_id = random.randint(1,4)
            query = '''SELECT titre, categorie_id, id
                        FROM greenimpact_question
                        WHERE categorie_id = %s ORDER BY RANDOM() LIMIT 1'''

            cursor.execute(query, [categorie_id])
            row = cursor.fetchone()
            print(row[2])
            if row[2] not in ids:
                print(len(ids))
                ids.append(row[2])
                query = "SELECT nom_categorie FROM greenimpact_categorie WHERE id = %s"
                cursor.execute(query, [row[1]])
                categories = cursor.fetchall()
                query = '''SELECT texte_option, valeur_carbone
                            FROM greenimpact_option
                            WHERE id IN (SELECT option_id
                                        FROM greenimpact_question_option
                                        WHERE question_id = %s);'''
                cursor.execute(query, [row[2]])
                options = cursor.fetchall()
                noms = [option[0] for option in options]
                valeurs = [option[1] for option in options]
                question = {
                    "titre" : row[0],
                    "categorie" : categories[0][0],
                    "options" : {
                        "noms" : noms,
                        "valeurs_carbonne" : valeurs,
                    }
                }
                questions.append(question)


    return JsonResponse(questions, safe=False)
