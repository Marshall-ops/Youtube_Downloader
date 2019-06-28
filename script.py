from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import os

dirpath = os.path.dirname(__file__)

url = input('Give the link of the video:')
url = url.replace('https://www.youtube.com','http://www.ssyoutube.com',1)


# Chrome Driver Options #
options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors')
options.add_argument('--ignore-certificate-errors')
#options.add_argument("--headless")
driver = webdriver.Chrome('%s\\Drivers\\chromedriver.exe' %dirpath, chrome_options = options)   #Path to Chrome Driver 

driver.get(url)

try:
    WebDriverWait(driver,30).until(
        EC.element_to_be_clickable((By.CLASS_NAME,"def-btn-box")))
    
    content = driver.page_source
    soup = BeautifulSoup(content,'lxml')

    div_content = soup.find('div',class_='def-btn-box')     #Div with Name and Link to Source Download
    link = div_content.find('a')['href']        #Geting Video Link
    name = div_content.find('a')['download']    #Geting Video Name
    media = requests.get(link,stream = True)    #Download Video File

    #Saving the File 
    print('Downloading the file.')
    with open("%s\\%s.mp4" %(dirpath, name),'wb') as f:
        for chunk in media.iter_content(chunk_size = 1024*1024): 
                if chunk: 
                    f.write(chunk)
    print('Video saved')
except :
    print('Can\'t find element')
    driver.close()

driver.quit()
