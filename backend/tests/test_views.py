from django.test import RequestFactory, TestCase
from django.urls import reverse

from greenimpact.views import start, accueil, result

class TestMyViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_start_view(self):
        request = self.factory.get('/start/')
        response = start(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'radioQuestion.html')
        self.assertTrue(len(response.context['questions']) == 8)

    def test_accueil_view(self):
        request = self.factory.get('/accueil/')
        response = accueil(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_result_view(self):
        request = self.factory.post('/result/')
        response = result(request)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {})
