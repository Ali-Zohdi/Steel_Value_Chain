import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

def GET_unit_subjects(URLs):

    s = Service(r"Z:\\HQ\BDM\\a.zohdi\\Data Engineering\\Github\\Geocoding\\chromedriver-win32\\chromedriver-win32\\chromedriver.exe")
    driver = webdriver.Chrome(service=s)

    url_id = 0
    units_list = []
    while url_id < len(URLs):

        driver.get(URLs[url_id])
        driver.set_window_size(1920, 1080)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        Subjects = soup.find_all(class_='d-flex m-1')
        headers = [subject.find('h3').text.strip() for subject in Subjects]

        unit_id = 0
        while unit_id in range(len(headers)):
            unit_id += 1

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            Unit_Click = driver.find_element(By.XPATH, f'//*[@id="mainPageContainer"]/div/div[2]/div/a[{unit_id}]/div')
            Unit_Click.click()
        
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            Units = soup.find_all(class_='d-flex m-1')
            unit_list = [unit.find('h3').text.strip() for unit in Units]

            if len(unit_list) == 0:
                units_list.append([url_id, headers[unit_id - 1], headers[unit_id - 1]])
            else:
                for i in range(len(unit_list)):
                    units_list.append([url_id, headers[unit_id - 1], unit_list[i]])    
    
            driver.back()
        
        url_id += 1

    units_list = pd.DataFrame(units_list, columns=['industry.id', 'subject', 'unit'])         

    return units_list

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
    
    industries = pd.DataFrame(industries, columns=['mother_industry', 'mother_industry_ENG', 'industry', 'URL'])

    return industries