from django.contrib.auth.models import Group, User
from django.test import TestCase, Client
from django.utils.http import quote_plus
from django.urls import reverse

from dashboard.models import Designation


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
   
# Designation View Test
class TestDesignationViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('ramesh','ramesh@gmail.com', 'ramesh')
        client = Client()
        self.list_url = reverse('dashboard:designations-list')

    def test_designation_list_with_login(self):
        self.client.login(username='ramesh', password='ramesh')
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/designations/list.html')

    def test_designation_list_without_login(self):
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, 302)

  
 # GroupRequired View Test
class TestGroupRequiredViews(TestCase):

    def setUp(self):
         #create permissions group
        group_name = "editor"
        self.group = Group(name=group_name)
        self.group.save()
        self.user = User.objects.create_user('ramesh','ramesh@gmail.com', 'ramesh')
        client = Client()
        self.list_url = reverse('dashboard:groups-list')

    def test_grouprequired_for_matching_group(self):
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='ramesh', password='ramesh')
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, 200)

    def test_grouprequired_for_not_matching_group(self):
        self.client.login(username='ramesh', password='ramesh')
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, 403)



