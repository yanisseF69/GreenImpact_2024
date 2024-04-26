''' This file contains the views for the GreenImpact app. '''

from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator


# Create your views here.

def start(request):
    '''
    This function is used to get the first 8 questions to display on the start page.
    '''

    page_number = request.GET.get('page', 1)  # Get the page number from the request
    questions_per_page = 1  
    total_questions_to_display = 10  

    with connection.cursor() as cursor:
        # Fetch the first 10 question IDs, types, and categories
        cursor.execute(
            '''SELECT id_typage, nom_typage, id_categ
               FROM greenimpact_typage
               ORDER BY id_typage ASC
               LIMIT %s''', [total_questions_to_display]
        )
        question_info = cursor.fetchall()

    # Prepare questions for pagination
    paginator = Paginator(question_info, questions_per_page)
    page_obj = paginator.get_page(page_number)

    # Prepare questions for the current page
    page_questions = []
    for id_typage, nom_typage, id_categ in page_obj:
        with connection.cursor() as cursor:
            # Fetch the question details
            cursor.execute(
                '''SELECT texte_question, type_question
                   FROM greenimpact_question 
                   WHERE id_typ = %s''', [id_typage]
            )
            quest = cursor.fetchone()

            # Fetch the category name
            cursor.execute(
                '''SELECT nom_categorie
                   FROM greenimpact_categorie 
                   WHERE id_categorie = %s''', [id_categ]
            )
            categorie = cursor.fetchone()

            # Fetch the options for the question
            cursor.execute(
                '''SELECT texte_option, empreinte_carbonne, id_option
                   FROM greenimpact_option
                   WHERE id_typ = %s LIMIT 5;''', [id_typage]
            )
            options = cursor.fetchall()

            # Construct the choices and the question dict
            choix = [{
                "id": option[2],
                "nom": option[0],
                "valeur": option[1],
            } for option in options]

            question = {
                "titre": quest[0],
                "categorie": categorie[0],
                "type": nom_typage,
                "choix": choix,
                "unique": quest[1] == 1,
            }
            page_questions.append(question)

    context = {
        'questions': page_questions,
        'page_obj': page_obj,  
    }
    return render(request, 'questions.html', context)


def index(request):
    """
    This function is just used to render the index page on the "/" route.
    """

    return render(request, 'index.html')


def result(request):
    '''
    This function is use to submit the answers and compute the final result.
    '''

    print("requete result")
    print(request)
    data = { }

    return JsonResponse(data)
