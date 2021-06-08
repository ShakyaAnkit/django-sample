import time
import selenium

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User 
from django.urls import reverse

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select


if hasattr(settings, 'SELENIUM_DRIVER_PATH'):
    class Setup(StaticLiveServerTestCase):
        
        def setUp(self):
            self.user = User.objects.create_superuser('ramesh','ramesh@gmail.com', 'ramesh')
            self.browser = webdriver.Chrome(settings.SELENIUM_DRIVER_PATH)

        def tearDown(self):
            self.browser.close()


    class TestLoginPage(Setup):

        def test_login_with_correct_credentials(self):
            self.browser.get(self.live_server_url)
            self.browser.find_element_by_id('id_username').send_keys("ramesh")
            self.browser.find_element_by_id('id_password').send_keys("ramesh")
            self.browser.find_element_by_tag_name('button').click()
            time.sleep(5)
            # checking if the user is redirected to home after login
            add_url= self.live_server_url + reverse('dashboard:index')
            self.assertEquals(self.browser.current_url, add_url)

        def test_login_with_incorrect_username(self):
            self.browser.get(self.live_server_url)
            self.browser.find_element_by_id('id_username').send_keys("wrong")
            self.browser.find_element_by_id('id_password').send_keys("ramesh")
            self.browser.find_element_by_tag_name('button').click()
            time.sleep(5)
            # checking validation error message
            self.assertEquals(self.browser.find_element_by_class_name('form-error').text, 'Incorrect username or password')
        
        def test_login_with_incorrect_password(self):
            self.browser.get(self.live_server_url)
            self.browser.find_element_by_id('id_username').send_keys("ramesh")
            self.browser.find_element_by_id('id_password').send_keys("wrong")
            self.browser.find_element_by_tag_name('button').click()
            time.sleep(5)
            # checking validation error message
            self.assertEquals(self.browser.find_element_by_class_name('form-error').text, 'Incorrect username or password')



    class TestDesignationFormPage(Setup):

        def test_create_designation(self):
            self.browser.get(self.live_server_url)
            self.browser.find_element_by_id('id_username').send_keys("ramesh")
            self.browser.find_element_by_id('id_password').send_keys("ramesh")
            self.browser.find_element_by_tag_name('button').click()
        
        # designation list view
            designation = self.browser.find_elements_by_class_name('sidebar-menu-text')[1]
            designation.click()

            # clicking add designation 
            self.browser.find_element_by_class_name('btn-outline-primary').click()

            # checking if it is redirected to form
            add_url = self.live_server_url + reverse('dashboard:designations-create')
            self.assertEquals(self.browser.current_url, add_url)
            
            # filling the designation form
            self.browser.find_element_by_name('name').send_keys("ramesh")
            self.browser.find_element_by_name('position').send_keys("designer")
            select = Select(self.browser.find_element_by_id("id_gender"))
            select.select_by_visible_text("MALE")

            # submitting form
            submit_button = self.browser.find_elements_by_tag_name('button')[1]
            submit_button.click()

            time.sleep(3)

            # # delete button click
            # self.browser.find_element_by_class_name('btn-danger').click()
            # # sweet alert conform click
            # self.browser.find_element_by_class_name('swal2-confirm').click()
            # time.sleep(2)

        
        def test_update_designation(self):
            self.test_create_designation()
            self.browser.find_element_by_class_name('btn-info').click()

            # filling the designation form
            self.browser.find_element_by_name('name').clear()
            self.browser.find_element_by_name('name').send_keys("sita")

            self.browser.find_element_by_name('position').clear()
            self.browser.find_element_by_name('position').send_keys("boss")

            select = Select(self.browser.find_element_by_id("id_gender"))
            select.select_by_visible_text("FEMALE")

            submit_button = self.browser.find_elements_by_tag_name('button')[1]
            submit_button.click()

            time.sleep(3)
    

    




        


