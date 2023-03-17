from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from subprocess import run #used to call programs from python
import os #used for talking to the OS
import urllib.parse #used to generate a url
import datetime

#unittest test class
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
        #variable that stores the current directory I am in
        current_dir = os.path.dirname(os.path.realpath(__file__))
        #variable that creates a path where the zip file will be stored.
        #the path is based off the current directory.
        zipPath = os.path.join(current_dir,f'{self.packageId}.zip')
        #variable that stores the directory of the files I am going to zip.
        packageRootDir = os.path.join(current_dir,'package_content')

        #remove existing package zip
        #in case it is still present in the path
        try:
            if os.path.exists(zipPath):
                print('removed existing zip')
                os.remove(zipPath)
        except OSError as e:
            print(f'Error removing zip: {zipPath} : {e}')
            raise e

        #Zip 3 files into a 7z package.
        #the run method takes arguments: 7z (program) - command a(add) -
        #path to zip to - path containing what should be zipped
        run(
            ['7z', 
            'a' ,
            zipPath, 
            os.path.join(packageRootDir, '*')] 
        )

        #Upload the package to the Tetrifact page
        #curl is a program for communicating via http
        #arguments used was found in the product documentation
        #https://github.com/shukriadams/tetrifact
        result = run(
            ['curl',
            '--silent',             
            '-X', 'POST', 
            '-H', 'Transfer-Encoding:chunked', 
            '-H', 'Content-Type:multipart/form-data', 
            '-F', f'Files=@{zipPath}',
            f'{self.tetrifactUrl}/v1/packages/{self.packageId}?IsArchive=true']
        )

        #Set PATH
        PATH = "D:\Tools\chromedriver110.exe"

        #Assign webdriver with PATH as argument, and setting
        #it to run headless, for shorter run time.
        options = Options()
        options.add_argument("--headless") 
        self.driver = webdriver.Chrome(PATH, options=options)
        
        #Ta bort cookies, om det funnits några.
        self.driver.delete_all_cookies()
    
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

        #finding the title element by class name
        title = self.driver.find_element(By.CLASS_NAME, "title")
        self.assertEqual(title.text,"Tetrifact Artifact storage")

    def test_upload_time(self):
        """
        Metod som kontrollerar att uppladdningstiden
        stämmer med nuvarande tid (inom 5 sek intervall). 
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
        element_file_size = self.driver.find_element(By.XPATH, "//div[contains(.,'Size')]/following-sibling::*") 
        #använder elementet för att få ut texten som
        #anger när uppladdningen skett, i str format
        file_size = element_file_size.text
        file_size = file_size.replace(",","")
        size_cleaned = int(file_size[0:4]) 

        self.assertEqual(size_cleaned, 1335)
    
        

    def test_tags(self):
        """
        Ger en tag till den uppladdade filen
        """

        #ger den uppladdade filen det hårdkodade värdet test_tag
        #the curl method i used to assign the tag value to the package
        #documentation on how to tag using curl is found in the product docs
        result = run([
            'curl',
            '-d',
            '-X', 'POST', 
            f'{self.tetrifactUrl}/v1/tags/test_tag/{self.packageId}'
            ])

        print(f'tag results:{result}')

        #deklararer ett värde för den webbsida vi vill nå
        url = urllib.parse.urljoin(self.tetrifactUrl, f"package/{self.packageId}", )
        #Load the package page
        self.driver.get(url)

        #En explicit wait för ett element för att säkerställa att
        #sidan börjat laddas. Inte en garanti för fulladdad sida, men
        #en basic check.
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "title")))

        #finner elementet med texten test_tag.
        element_file_tag = self.driver.find_element(By.XPATH, "//a[contains(.,'test_tag')]")
        
        #asserterar att den skapade taggen har förväntat värde
        self.assertEqual(element_file_tag.text, "test_tag")
        

    def test_file_names(self):
        """
        Metod som asserterar att de filnamn som visas på
        hemsidan, innehåller de förväntade hårdkodade 
        filnamnen. 
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
        
        #finner elementet med texten test_tag.
        element_file_names = self.driver.find_elements(By.CLASS_NAME, "listItem-text")

        file_names = []
        for element in element_file_names:
            file_names.append(element.text)
            
        #assert that there are 3 elements in the array
        #corresponding to the 3 uploaded files
        self.assertEqual(len(element_file_names), 3)

        #asserts that the file names are all found in the array
        self.assertNotEqual(file_names.index("file01.txt"), -1)
        self.assertNotEqual(file_names.index("file02.txt"), -1)
        self.assertNotEqual(file_names.index("file03.txt"), -1)


    def tearDown(self) -> None:
        """
        Tearing down the test:
        Closing the driver and removing 
        uploaded package.
        """
        
        #Stänger webdrivern
        self.driver.quit()

        #tar bort det uppladdade paketet
        #uses curl to delete the package on the server
        #documentation on how to delete is found in the product docs
        run(
            ['curl',
            '--silent',             
            '-X', 'DELETE', 
            f'{self.tetrifactUrl}/v1/packages/{self.packageId}']
        )

        return super().tearDown()


