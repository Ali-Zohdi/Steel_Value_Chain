from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

url = 'https://infosaba.com/industries/آهن-و-فولاد'
s = Service(r"Z:\\HQ\BDM\\a.zohdi\\Data Engineering\\Github\\Geocoding\\chromedriver-win32\\chromedriver-win32\\chromedriver.exe")

driver = webdriver.Chrome(service=s)
driver.get(url)
driver.set_window_size(1920, 1080)

def sub_industries():

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    elements = soup.find_all(class_='d-flex m-1')
    hrefs = [element.find('h3').text.strip() for element in elements]

    print('title', hrefs)

    sub_ind_id = 0
    sub_industry_list = []
    while sub_ind_id in range(len(hrefs)):
        sub_ind_id += 1

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sub_industry_click = driver.find_element(By.XPATH, f'//*[@id="mainPageContainer"]/div/div[2]/div/a[{sub_ind_id}]/div')
        sub_industry_click.click()
       
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        elements = soup.find_all(class_='d-flex m-1')
        hrefs_2 = [element.find('h3').text.strip() for element in elements]

        if len(hrefs_2) == 0:
            sub_industry_list.append([hrefs[sub_ind_id - 1], hrefs[sub_ind_id]])
        else:
            for i in range(len(hrefs_2)):
                sub_industry_list.append([hrefs[sub_ind_id - 1], hrefs_2[i]])    
   
        print(sub_industry_list)
        driver.back()           

    return sub_industry_list

mylist = sub_industries()
print(len(mylist))