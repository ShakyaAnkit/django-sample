from django.test import TestCase, Client
from django.utils.http import quote_plus
from django.urls import reverse

from dashboard.views import DesignationListView, DesignationCreateView, DesignationUpdateView
from dashboard.models import Designation, User

# Designation View Test
class TestDesignationWithoutLoginViews(TestCase):

    def setUp(self):
        self.designation = Designation.objects.create(
            name = 'Luis Suarez',
            position = 'Striker',
            gender = 'MALE',
            date_of_birth = '2020-01-12'
        )
        client = Client()
        self.list_url = reverse('dashboard:designations-list')

    def test_designation_list_GET(self):
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, 302)

class TestDesignationViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('ramesh','ramesh@gmail.com', 'ramesh')
        client = Client()
        self.list_url = reverse('dashboard:designations-list')

    def test_designation_list_for_authorized_user(self):
        self.client.login(username='ramesh', password='ramesh')
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/designations/list.html')


    def test_designation_list_for_unauthorized_user(self):
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, 302)


class TestLoginView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('ramesh','ramesh@gmail.com', 'ramesh')
        client = Client()
        self.login_url = reverse('dashboard:login')

    def test_user_login_page(self):
        response = self.client.get(self.login_url)
        self.assertTemplateUsed(response, 'dashboard/auth/login.html')
    
    def test_user_correct_login(self):
        login = self.client.login(username='ramesh', password='ramesh')
        self.assertTrue(login) 
    
    def test_wrong_username_login(self):
        login = self.client.login(username='wrong', password='ramesh')
        self.assertFalse(login) 
    
    def test_wrong_password_login(self):
        login = self.client.login(username='ramesh', password='wrong')
        self.assertFalse(login) 
    
    def test_user_logged_in(self):
        self.client.login(username='ramesh', password='ramesh')
        response = self.client.get(self.login_url, follow=True)
        user = User.objects.get(username='ramesh')

        # Check if user is logged in
        self.assertEqual(response.context['user'].email, 'ramesh@gmail.com')

       # Check if response is "success"
        self.assertEqual(response.status_code, 200)
    
    ## Request a logout after logging in
    def test_logout(self):
        # Log in
        self.client.login(username='ramesh', password='ramesh')

        # Request a page that requires a login
        response = self.client.get(reverse('dashboard:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].username, 'ramesh')

        # Log out
        self.client.logout()

        # Request a page that requires a login
        response = self.client.get(reverse('dashboard:designations-list'))
        self.assertEqual(response.status_code, 302)
        directorate_login_url = reverse('dashboard:login')+'?next='+quote_plus(reverse('dashboard:designations-list'))
        self.assertRedirects(response, directorate_login_url)

    
  
    

