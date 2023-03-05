from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from subprocess import run
import os
import urllib.parse
import datetime
import re

class myTestClass(TestCase):
    
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        #class variables
        self.driver = None
        self.tetrifactUrl = 'https://testrifact.manafeed.com'
        self.packageId = 'test_package'

    def setUp(self):
        """
        setting up the test:

        Upload said package to Tetrifact page.
        Set PATH and assign the webdriver.
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

        #Zip 3 files into a 7z package.
        result = run(
            ['7z', 
            'a' ,
            zipPath, 
            os.path.join(packageRootDir, '*')] 
        )

        #Upload the package to the Tetrifact page
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

        #Set PATH
        PATH = "D:\Tools\chromedriver110.exe"

        #Assign webdriver with PATH as argument
        self.driver = webdriver.Chrome(PATH)
    
    def test_title_text(self):
        """
        Testmetod för att få till ett första lyckat test,
        att sidans Titeltext matchar det förväntade värdet.
        """   

        #Load the Tetrifact page
        self.driver.get(self.tetrifactUrl)

        #En explicit wait för ett element för att säkerställa att
        #sidan börjat laddas. Inte en garanti för fulladdad sida, men
        #en basic check.
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "title")))

        title = self.driver.find_element(By.CLASS_NAME, "title")
        self.assertEqual(title.text,"Tetrifact Artifact storage")

    def test_upload_time(self):
        """
        Metod som kontrollerar att uppladdningstiden
        stämmer med nuvarande tid (inom 1 min intervall). 
        """

        #deklararer ett värde för den webbsida vi vill nå
        url = urllib.parse.urljoin(self.tetrifactUrl, f"package/{self.packageId}", )
        #Load the package page
        self.driver.get(url)

        #En explicit wait för ett element för att säkerställa att
        #sidan börjat laddas. Inte en garanti för fulladdad sida, men
        #en basic check.
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "title")))
        
        #finner elementet med texten Created.
        element_created = self.driver.find_element(By.XPATH, "//div[contains(.,'Created')]/following-sibling::*") # 
        #använder elementet för att få ut texten som
        #anger när uppladdningen skett, i str format
        date = element_created.text

        #rensar strängen
        date_cleaned = date[0:16] 

        #konverterar strängen till datetimeformat
        date_as_datetime = datetime.datetime.strptime(date_cleaned, '%Y-%m-%d %H:%M')
        
        #asserterar att uppladdningstiden är inom 5 sec från asserteringstiden
        #(en basic koll för att checka att tiden stämmer )
        self.assertAlmostEqual(datetime.datetime.now(), date_as_datetime, delta=datetime.timedelta(seconds=5000))


    def test_file_count(self):
        """
        Metod som kontrollerar att det antal filer som visas
        motsvarar det faktiska antalet uppladdade filer i paketet.
        """

        #deklararer ett värde för den webbsida vi vill nå
        url = urllib.parse.urljoin(self.tetrifactUrl, f"package/{self.packageId}", )
        #Load the package page
        self.driver.get(url)

        #En explicit wait för ett element för att säkerställa att
        #sidan börjat laddas. Inte en garanti för fulladdad sida, men
        #en basic check.
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "title")))
        
        #finner elementet med texten Created.
        element_count = self.driver.find_element(By.XPATH, "//div[contains(.,'File count')]/following-sibling::*") # 
        #använder elementet för att få ut texten som
        #anger när uppladdningen skett, i str format
        file_count = element_count.text

        #Antalet filer jag använder för testet är 3, 
        #detta värde är därför hårdkodat.
        self.assertEqual(int(file_count), 3)


    def test_file_size(self):
        
        """
        Metod som kontrollerar att paketstorleken som visas
        motsvarar det faktiska antalet uppladdade filer i paketet.
        """

        #deklararer ett värde för den webbsida vi vill nå
        url = urllib.parse.urljoin(self.tetrifactUrl, f"package/{self.packageId}", )
        #Load the package page
        self.driver.get(url)

        #En explicit wait för ett element för att säkerställa att
        #sidan börjat laddas. Inte en garanti för fulladdad sida, men
        #en basic check.
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "title")))
        
        #finner elementet med texten Created.
        element_file_size = self.driver.find_element(By.XPATH, "//div[contains(.,'Size')]/following-sibling::*") # 
        #använder elementet för att få ut texten som
        #anger när uppladdningen skett, i str format
        file_size = element_file_size.text
        file_size = file_size.replace(",","")
        size_cleaned = int(file_size[0:4]) 

        self.assertEqual(size_cleaned, 1335)
    
        
    """
    def test_tags(self):
        pass

    def test_file_names(self):
        pass
    """

    def tearDown(self) -> None:
        pass
        """
        Tearing down the test:
        Closing the driver and removing 
        uploaded package.
        """
        self.driver.quit()


        run(
            ['curl',
            '--write-out', '%{http_code}%', 
            '--silent',             
            '-X', 'DELETE', 
            f'{self.tetrifactUrl}/v1/packages/{self.packageId}']
        )

        return super().tearDown()


