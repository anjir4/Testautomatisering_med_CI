from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
PATH = "D:\Tools\chromedriver.exe"
driver = webdriver.Chrome(PATH) # Optional argument, if not specified will search path.

#This will open this webpage
#driver.get("https://tetrifact.manafeed.com/")

#This will print the web page title in the output window
#print(driver.title)

#This will close the webpage
#driver.quit()

#This will send keys Chromedriver to element search_box
#search_box.send_keys('ChromeDriver')

#this will submit element seach box?
#search_box.submit()

class basePageObjectTest(TestCase):
    pass


    def setUp(self):
        pass
        """
        setting up the test
        """
        #New_library_app.borrowers = {}
    
    """
    def test_class_name_title(self):

        driver.get('https://www.google.com/')

        time.sleep(5) # Let the user actually see something!

        #title = driver.find_elements_by_class_name('title')
        title = driver.find_element(By.CLASS_NAME, "title")
        text = title.get_attribute('innerText')
        
        time.sleep(5) # Let the user actually see something!
        driver.quit()
    """
    def test_google(self):

        driver.get('https://tetrifact.manafeed.com/')

        time.sleep(5) # Let the user actually see something!

        #title = driver.find_elements_by_class_name('title')
        title = driver.find_element(By.CLASS_NAME, "title")
        text = title.get_attribute('innerText')
        
        time.sleep(5) # Let the user actually see something!
        driver.quit()


