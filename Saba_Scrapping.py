import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

def sub_industries():

    url = 'https://infosaba.com/industries/آهن-و-فولاد'
    s = Service(r"Z:\\HQ\BDM\\a.zohdi\\Data Engineering\\Github\\Geocoding\\chromedriver-win32\\chromedriver-win32\\chromedriver.exe")

    driver = webdriver.Chrome(service=s)
    driver.get(url)
    driver.set_window_size(1920, 1080)

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

# mylist = sub_industries()
# print(len(mylist))


def GET_industries():

    url = 'https://infosaba.com'
    s = Service(r"Z:\\HQ\BDM\\a.zohdi\\Data Engineering\\Github\\Geocoding\\chromedriver-win32\\chromedriver-win32\\chromedriver.exe")

    driver = webdriver.Chrome(service=s)
    driver.get(url)
    driver.set_window_size(1920, 1080)

    i = 1
    industries = []

    while i > 0:
        try:
            mother_industry = driver.find_element(By.XPATH, f'//*[@id="mainPageContainer"]/div[2]/div[2]/div[{i}]/a/div/div')
            industry = mother_industry.text.split('\n')

            mother_industry.click()

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            sub_industries = soup.find_all(class_='d-flex m-1')

            sub_ind = 0
            while sub_ind in range(len(sub_industries)):
                sub_ind += 1

                time.sleep(3)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sub_industry = driver.find_element(By.XPATH, f'//*[@id="mainPageContainer"]/div/div[2]/div/a[{sub_ind}]')
                url = sub_industry.get_attribute('href')

                ind = sub_industries[sub_ind - 1].find('h3').text.strip()

                industries.append([industry[0], industry[1], ind, url])

            driver.back()
            i += 1
        except:
            break
    
    industries = pd.DataFrame(industries, columns=['mother_industry_name', 'mother_industry_ENG_name', 'name', 'URL'])

    return industries