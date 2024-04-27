''' This file contains the views for the GreenImpact app. '''

import logging
from django.db import connection
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.urls import reverse
from django.http import JsonResponse
import matplotlib.pyplot as plt




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

def get_category_id_from_type(type_name):
    """
    Get the ID of the category using the type name.

    Parameters:
    type_name (str): The name of the type.

    Returns:
    str: The ID of the type's category.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            '''SELECT id_categ
               FROM greenimpact_typage 
               WHERE nom_typage = %s''', [type_name]
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

def get_valeur(option_name):
    """
    Retrieve the value of an option using its name.

    Parameters:
    option_name (str): The name of the question type.

    Returns:
    list: A list of tuples containing the options' text, carbon footprint, and ID.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            '''SELECT empreinte_carbonne
               FROM greenimpact_option
               WHERE texte_option = %s;''', [option_name]
        )
        return cursor.fetchone()

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
            #     logger.debug("Received for %s: %s", key, values)
            # logger.debug("Received for: %s", request.session['responses'])
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
    results = { }
    for reponse in all_responses:
        typage = reponse[:-2]
        id_categorie = get_category_id_from_type(typage)
        nom_categorie = get_category_name(id_categorie)[0]
        for choix in all_responses[reponse]:
            if nom_categorie not in results:
                results[nom_categorie] = 0
            results[nom_categorie] += int(get_valeur(choix)[0])

    return results

def get_category_avg_carbon_footprint(request):
    """
    Retrieve average carbon footprints for each category from the database.
    
    Parameters:
    request (HttpRequest): The HTTP request object.
    
    Returns:
    JsonResponse: A JSON response containing category names 
                  as keys and average carbon footprints as values.
    """
    category_data = {}
    with connection.cursor() as cursor:
        cursor.execute('SELECT nom_categorie FROM greenimpact_categorie')
        categories = cursor.fetchall()
        for category in categories:
            cursor.execute('''
                SELECT t.nom_typage, AVG(o.empreinte_carbonne)
                FROM public.greenimpact_categorie c
                INNER JOIN public.greenimpact_typage t ON c.id_categorie = t.id_categ
                INNER JOIN public.greenimpact_option o ON t.id_typage = o.id_typ
                WHERE c.nom_categorie = %s
                GROUP BY t.nom_typage;
            ''', [category[0]])
            typage_avg_empreinte_carbonne = cursor.fetchall()
            category_data[category[0]] = typage_avg_empreinte_carbonne
    return JsonResponse(category_data)

def generate_pie_charts(category_data):
    """
    Generate pie charts for each category based on the provided data and display them.
    
    Parameters:
    category_data (dict): A dictionary containing category names as keys and 
    lists of tuples containing typage names and average carbon footprints as values.
    """
    for category, typage_data in category_data.items():
        typages = [typage[0] for typage in typage_data]
        carbon_percentages = [typage[1] for typage in typage_data]
        plt.figure(figsize=(8, 8))
        plt.pie(carbon_percentages, labels=typages, autopct='%1.1f%%')
        plt.title(f'Diagramme circulaire pour {category}')
        plt.show()
        plt.close()
