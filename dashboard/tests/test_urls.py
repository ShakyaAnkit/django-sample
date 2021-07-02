from django.test import SimpleTestCase
from django.urls import reverse,resolve

from dashboard.views import DesignationListView, DesignationCreateView, DesignationUpdateView, DesignationDeleteView, LoginPageView, LogoutView


 # Login Url Test
class TestLoginUrls(SimpleTestCase): 
    def test_login_url_is_resolved(self):
        url = reverse('dashboard:login')
        self.assertEquals(resolve(url).func.view_class, LoginPageView)

# Logout Url Test
class TestLogoutUrls(SimpleTestCase): 
    def test_logout_url_is_resolved(self):
        url = reverse('dashboard:logout')
        self.assertEquals(resolve(url).func.view_class, LogoutView)
    
# Invalid Url Test
class TestInvalidUrls(SimpleTestCase):
    def test_unknown_page(self):
        #GET an invalid URL
        response = self.client.get('/unknown_view/')
        self.assertEqual(response.status_code, 404)

# Designation Url Test
class TestDesignationUrls(SimpleTestCase):

    def test_designation_list_url_is_resolved(self):
        url = reverse('dashboard:designations-list')
        self.assertEquals(resolve(url).func.view_class, DesignationListView)
    
    def test_designation_create_url_is_resolved(self):
        url = reverse('dashboard:designations-create')
        self.assertEquals(resolve(url).func.view_class, DesignationCreateView)
    
    def test_designation_detail_url_is_resolved(self):
        url = reverse('dashboard:designations-update', kwargs={ 'pk': '1'})
        self.assertEquals(resolve(url).func.view_class, DesignationUpdateView)
    
    def test_designation_delete_url_is_resolved(self):
        url = reverse('dashboard:designations-delete', kwargs={ 'pk': '1'})
        self.assertEquals(resolve(url).func.view_class, DesignationDeleteView)


