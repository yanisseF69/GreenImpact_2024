""" This module tests the views in the greenimpact app. """
from django.test import TestCase, Client
from django.urls import reverse

class TestMyViews(TestCase):
    """ 
    This class tests the views in the greenimpact app.
    It tests the views start, accueil and result.
    """
    def setUp(self):
        self.client = Client()

    def test_start_view(self):
        """ Test the start view."""
        response = self.client.get(reverse('start') + '?page=1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'questions.html')

    def test_result_view(self):
        """ Test the result view."""
        # Simulate POST request data
        data = {
            'Salade[]': ['Blette'],  # Exemple de réponse à la première page
            # Ajoutez les réponses pour les autres pages si nécessaire
        }
        response = self.client.post(reverse('result'), data)
        self.assertEqual(response.status_code, 302)  # Redirection après envoi du formulaire
