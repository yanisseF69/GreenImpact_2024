''' This file contains the views for the GreenImpact app. '''

from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator


# Create your views here.

def get_question_info(total_questions_to_display):
    with connection.cursor() as cursor:
        cursor.execute(
            '''SELECT id_typage, nom_typage, id_categ
               FROM greenimpact_typage
               ORDER BY id_typage ASC
               LIMIT %s''', [total_questions_to_display]
        )
        return cursor.fetchall()

def get_question_details(id_typage):
    with connection.cursor() as cursor:
        cursor.execute(
            '''SELECT texte_question, type_question
               FROM greenimpact_question 
               WHERE id_typ = %s''', [id_typage]
        )
        return cursor.fetchone()

def get_category_name(id_categ):
    with connection.cursor() as cursor:
        cursor.execute(
            '''SELECT nom_categorie
               FROM greenimpact_categorie 
               WHERE id_categorie = %s''', [id_categ]
        )
        return cursor.fetchone()

def get_options(id_typage):
    with connection.cursor() as cursor:
        cursor.execute(
            '''SELECT texte_option, empreinte_carbonne, id_option
               FROM greenimpact_option
               WHERE id_typ = %s LIMIT 5;''', [id_typage]
        )
        return cursor.fetchall()

def prepare_questions(question_info):
    questions = []
    for id_typage, nom_typage, id_categ in question_info:
        quest = get_question_details(id_typage)
        categorie = get_category_name(id_categ)
        options = get_options(id_typage)
        choix = [{"id": option[2], "nom": option[0], "valeur": option[1]} for option in options]
        questions.append({
            "titre": quest[0],
            "categorie": categorie[0],
            "type": nom_typage,
            "choix": choix,
            "unique": quest[1] == 1,
        })
    return questions

def start(request):
    page_number = request.GET.get('page', 1)
    questions_per_page = 1
    total_questions_to_display = 10

    question_info = get_question_info(total_questions_to_display)
    paginator = Paginator(question_info, questions_per_page)
    page_obj = paginator.get_page(page_number)
    page_questions = prepare_questions(page_obj.object_list)

    context = {'questions': page_questions, 'page_obj': page_obj}
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
