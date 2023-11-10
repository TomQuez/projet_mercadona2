from django.test import TestCase
from django.template import Context, Template

class TemplateTests(TestCase):
    def test_index2_template(self):
        response=self.client.get('index2')
        self.assertEqual(response.status_code,200)
        
        self.assertContains(response,'Catalogue Mercadona')
        self.assertContains(response,'Bienvenue sur le catalogue de Mercadona')
        