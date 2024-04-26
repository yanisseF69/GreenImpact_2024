''' This file contains the views for the GreenImpact app. '''

import logging
from django.db import connection
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.urls import reverse


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def get_question_info(total_questions_to_display):
    """
    Fetch the first set of question IDs, types, and categories for the quiz.

    Parameters:
    total_questions_to_display (int): The total number of questions to display.

    Returns:
    list: A list of tuples containing the question IDs, types, and categories.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            '''SELECT id_typage, nom_typage, id_categ
               FROM greenimpact_typage
               ORDER BY id_typage ASC
               LIMIT %s''', [total_questions_to_display]
        )
        return cursor.fetchall()

def get_question_details(id_typage):
    """
    Retrieve the details of a question using its ID.

    Parameters:
    id_typage (int): The ID of the question.

    Returns:
    tuple: A tuple containing the text and the type of the question.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            '''SELECT texte_question, type_question
               FROM greenimpact_question 
               WHERE id_typ = %s''', [id_typage]
        )
        return cursor.fetchone()

def get_category_name(id_categ):
    """
    Get the name of the category using the category ID.

    Parameters:
    id_categ (int): The ID of the category.

    Returns:
    str: The name of the category.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            '''SELECT nom_categorie
               FROM greenimpact_categorie 
               WHERE id_categorie = %s''', [id_categ]
        )
        return cursor.fetchone()

def get_options(id_typage):
    """
    Retrieve the options for a question using its type ID.

    Parameters:
    id_typage (int): The ID of the question type.

    Returns:
    list: A list of tuples containing the options' text, carbon footprint, and ID.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            '''SELECT texte_option, empreinte_carbonne, id_option
               FROM greenimpact_option
               WHERE id_typ = %s LIMIT 5;''', [id_typage]
        )
        return cursor.fetchall()

def prepare_questions(question_info):
    """
    Prepare the list of questions with their details and options for pagination.

    Parameters:
    question_info (list): A list of tuples containing question information.

    Returns:
    list: A list of dictionaries, each representing a question and its choices.
    """
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
    """
    The view function for the start page that renders the first 10 paginated questions.

    Parameters:
    request (HttpRequest): The HTTP request object.

    Returns:
    HttpResponse: The HTTP response object with the rendered template for the start page.
    """
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
    """
    Process and store user responses on each page of the questionnaire, 
    and compute final results at the end.

    This function handles form submissions for each page of a multi-page questionnaire.
    It stores responses in the session, once the final page is submitted,
    it aggregates all responses, computes the final results, and displays the results page. 

    Parameters:
    request (HttpRequest): The incoming request object from the user.

    Returns:
    HttpResponse: Redirects to the next page of the questionnaire if not the last page,
                   or renders the results page with the computed data if it's the last page.
                   If the method is not POST, redirects to the index page.
    """
    if request.method == 'POST':
        if 'responses' not in request.session:
            request.session['responses'] = {}
        for key in request.POST.keys():
            if key.endswith('[]'):
                values = request.POST.getlist(key)
                request.session['responses'][key] = values
                logger.debug("Received for %s: %s", key, values)
            logger.debug("Received for: %s", request.session['responses'])
        page_number = request.POST.get('page_number')
        request.session.modified = True

        if int(page_number) == 10:
            result_data = compute_results(request.session['responses'])
            request.session.flush()
            return render(request, 'results.html', {'result_data': result_data})

        next_page = int(page_number) + 1
        return redirect(f'{reverse("start")}?page={next_page}')

    return redirect('index')

def compute_results(all_responses):
    """
    Combine and compute the final results from the data of all pages.

    Parameters:
    all_responses (dict): Dictionary of responses from all pages.

    Returns:
    dict: A dictionary with the results of the computations.
    """

    # Fusionner les réponses ou calculer sur la base des réponses collectées
    # Retourner un dictionnaire avec les résultats
    return {}
