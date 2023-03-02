from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

        try:
            #making sure this object has loaded, as then we can assume that this
            #relatively simple page has fully loaded and is ready for testing. 
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q")))

            country_button = driver.find_element(By.NAME, "btnK")
            button_text = country_button.get_attribute("value")
            ## button_text  == Google-søgning
            self.assertEqual(button_text,"Google-søgning")

        finally:
            driver.quit()


