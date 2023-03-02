from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
PATH = "D:\Tools\chromedriver110.exe"
driver = webdriver.Chrome(PATH) # Optional argument, if not specified will search path.

"""
Test to make sure my test setup works with the IDE and the webdriver
02/03/23
"""

class basePageObjectTest(TestCase):
    #pass


    def setUp(self):
        pass
        """
        setting up the test
        """
        #New_library_app.borrowers = {}
    
    def test_google(self):

        driver.get('https://google.com/')

        time.sleep(5) # Let the user actually see something!

        #title = driver.find_elements_by_class_name('title')
        search_box = driver.find_element(By.NAME, "q")
        country_button = driver.find_element(By.NAME, "btnK")
        button_text = country_button.get_attribute("value")
        ## button_text  == Google-søgning
        self.assertEqual(button_text,"Google-søgning")

        time.sleep(5) # Let the user actually see something!
        driver.quit()


