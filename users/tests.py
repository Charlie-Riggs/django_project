from django.test import TestCase
from django.urls import reverse


class LoginFlowTests(TestCase):
    def test_login_page_preserves_next_destination(self):
        response = self.client.get(reverse('users:login'), {'next': '/topics'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="/topics"')
