from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

url = 'https://infosaba.com/industries/آهن-و-فولاد'
s = Service(r"Z:\\HQ\BDM\\a.zohdi\\Data Engineering\\Github\\Geocoding\\chromedriver-win32\\chromedriver-win32\\chromedriver.exe")

driver = webdriver.Chrome(service=s)
driver.get(url)

def sub_industries():

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    elements = soup.find_all(class_='d-flex m-1')
    hrefs = [element.find('h3').text.strip() for element in elements]

    print('title', hrefs)

    sub_ind_id = 0
    while sub_ind_id in range(len(hrefs)):
        sub_ind_id += 1
        print(sub_ind_id)
        
        sub_industry_click = driver.find_element(By.XPATH, f'//*[@id="mainPageContainer"]/div/div[2]/div/a[{sub_ind_id}]/div/span')
        sub_industry_click.click()
#       try:
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        elements = soup.find_all(class_='d-flex m-1')
        hrefs_2 = [element.find('h3').text.strip() for element in elements]
        # if len(hrefs_2) == 0:
        #     print("no sub industry")
        # else:   
        print(hrefs_2)
        driver.implicitly_wait(400)
        driver.back()
        driver.implicitly_wait(400)            
        # except:
        #     # header = driver.find_element(By.XPATH, '//*[@id="ajaxcontent"]/div[1]/h3')
        #     # print(header.text)    
        #     print("no sub industry!!!!")
        #     driver.back()


sub_industries()