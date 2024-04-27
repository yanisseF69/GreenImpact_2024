""" Tests for views in greenimpact app. """
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

from greenimpact.views import start, result # accueil

@override_settings(DATABASES={'default': {'NAME': 'test_mif10'}})
class TestMyViews(TestCase):
    """ 
    This class tests the views in the greenimpact app.
    It tests the views start, accueil and result.
    """
    def setUp(self):
        self.factory = RequestFactory()

    def test_start_view(self):
        """ Test the start view."""
        request = self.factory.get('/start/')
        response = start(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'radioQuestion.html')
        self.assertTrue(len(response.content['questions']) == 8)

    # def test_accueil_view(self):
    #     """ Test the accueil view."""
    #     request = self.factory.get('/accueil/')
    #     response = accueil(request)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'index.html')

    def test_result_view(self):
        """ Test the result view."""
        request = self.factory.post('/result/')
        response = result(request)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {})
