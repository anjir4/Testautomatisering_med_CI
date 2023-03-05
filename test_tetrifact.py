from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from subprocess import run
import os

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
    
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.driver = None
        self.tetrifactUrl = 'https://testrifact.manafeed.com'
        self.packageId = 'test_package'

    def setUp(self):
        """
        setting up the test
        """
        dir_path = os.path.dirname(os.path.realpath(__file__))

        zipPath = os.path.join(dir_path,f'{self.packageId}.zip')
        packageRootDir = os.path.join(dir_path,'package_content')


        tag = 'mytag'
        
        # remove existing package zip
        try:
            if os.path.exists(zipPath):
                print('removed existing zip')
                os.remove(zipPath)
        except OSError as e:
            print(f'Error removing zip: {zipPath} : {e}')
            raise e

        result = run(
            ['7z', 
            'a' ,
            zipPath, 
            os.path.join(packageRootDir, '*')] 
        )

        print(f'zip results:{result}')

        result = run(
            ['curl',
            '--write-out', '%{http_code}%', 
            '--silent',             
            '-X', 'POST', 
            '-H', 'Transfer-Encoding:chunked', 
            '-H', 'Content-Type:multipart/form-data', 
            '-F', f'Files=@{zipPath}',
            f'{self.tetrifactUrl}/v1/packages/{self.packageId}?IsArchive=true']
        )

        print(f'upload results:{result}')

        PATH = "D:\Tools\chromedriver110.exe"
        self.driver = webdriver.Chrome(PATH) # Optional argument, if not specified will search path.

        self.driver.get(self.tetrifactUrl)

        #Documentation for select By
        #https://selenium-python.readthedocs.io/locating-elements.html 
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "title")))
    
    def test_title_text(self):

        #making sure this object has loaded, as then we can assume that this
        #relatively simple page has fully loaded and is ready for testing.

        title = self.driver.find_element(By.CLASS_NAME, "title")
        self.assertEqual(title.text,"Tetrifact Artifact storage")

    def tearDown(self) -> None:
        self.driver.quit()

        run(
            ['curl',
            '--write-out', '%{http_code}%', 
            '--silent',             
            '-X', 'DELETE', 
            f'{self.tetrifactUrl}/v1/packages/{self.packageId}']
        )

        return super().tearDown()


