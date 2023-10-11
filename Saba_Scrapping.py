import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

    unit = list(units_list['unit'])
    unit_urls = []

    for u in unit:
        url_ = u.replace('(', '').replace(')', '').replace(' ', '-')
        url_text = f'https://infosaba.com/Unit_Subjects/{url_}'
        unit_urls.append(url_text)

    units_list['URL'] = unit_urls         

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
    
    industries = pd.DataFrame(industries, columns=['mother_industry', 'mother_industry_ENG', 'name', 'URL'])

    return industries


def GET_complexes():
    
    url = 'https://infosaba.com/complexes/showlist'
    s = Service(r"Z:\\HQ\BDM\\a.zohdi\\Data Engineering\\Github\\Geocoding\\chromedriver-win32\\chromedriver-win32\\chromedriver.exe")

    driver = webdriver.Chrome(service=s)
    driver.get(url)
    driver.set_window_size(1920, 1080)

    card_list = driver.find_element(By.ID, 'counter-cards')

    while True:
        before_scroll = len(card_list.find_elements(By.CLASS_NAME, 'd-none'))
        driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
        time.sleep(3)
        after_scroll = len(card_list.find_elements(By.CLASS_NAME, 'd-none'))
        if after_scroll == before_scroll:
            break    

    Complexes = card_list.find_elements(By.CLASS_NAME, 'counter-card')
    complex_list = [complexes.text.strip().split('\n') for complexes in Complexes]

    complex_list = pd.DataFrame(complex_list, columns=['city', 'name', 'industry.name'])

    return complex_list


def GET_unit_complex(URLs):

    s = Service(r"Z:\\HQ\BDM\\a.zohdi\\Data Engineering\\Github\\Geocoding\\chromedriver-win32\\chromedriver-win32\\chromedriver.exe")
    driver = webdriver.Chrome(service=s)

    unit_complex_complete = [['unit.id', 'unit.url', 'complex.name', 'capacity', 'capacity_Tons', 'capacity_measure', 'under_construction', 'under_construction_Tons', 'under_construction_measure']]
    url_id = 0
    while url_id < len(URLs):
        url = URLs[url_id]
        driver.get(url)
        driver.set_window_size(1920, 1080)
        time.sleep(3)

        complex_list_container = driver.find_element(By.ID, 'ajaxcontent')
        complex_list = complex_list_container.find_elements(By.CSS_SELECTOR, 'div.d-flex.flex-wrap.flex-md-row.justify-content-center.mt-4.px-0 > div')

        #Check for Complexes
        if len(complex_list) == 0:
            print(f'There is no Complex in this link: {url}')
            url_id += 1
            continue

        showall_button = driver.find_element(By.ID, 'showallbutton')
        showall_button.click()

        while True:
            before_scroll = len(complex_list_container.find_elements(By.CLASS_NAME, 'w-md-100'))
            driver.execute_script("window.scrollBy(0,document.body.scrollHeight);")
            time.sleep(2)
            after_scroll = len(complex_list_container.find_elements(By.CLASS_NAME, 'w-md-100'))
            if after_scroll == before_scroll:
                break 
        
        Complexes = complex_list_container.find_elements(By.CLASS_NAME, 'w-md-100')
        complex_list = [complexes.text.strip().split('\n') for complexes in Complexes]

        pages = complex_list_container.find_elements(By.CLASS_NAME, 'page-link')
        if len(pages) < 2:
            pass
        else :
            page = 1
            while page < len(pages):
                page += 1
                driver.execute_script(f'mptmodulesrefresh({page});')
                complex_list_container = driver.find_element(By.ID, 'ajaxcontent')
                while True:
                    before_scroll = len(complex_list_container.find_elements(By.CLASS_NAME, 'w-md-100'))
                    driver.execute_script("window.scrollBy(0,document.body.scrollHeight);")
                    time.sleep(2)
                    after_scroll = len(complex_list_container.find_elements(By.CLASS_NAME, 'w-md-100'))
                    if after_scroll == before_scroll:
                        break 
                Complexes = complex_list_container.find_elements(By.CLASS_NAME, 'w-md-100')
                current_page_complex_list = [complexes.text.strip().split('\n') for complexes in Complexes]
                complex_list.extend(current_page_complex_list)
        
        Unit_Complex = [[url_id, url] + sublist for sublist in complex_list]
        unit_complex_complete.extend(Unit_Complex)
        url_id += 1

    Unit_Complex_list = pd.DataFrame(unit_complex_complete[1:], columns=unit_complex_complete[0])
    Unit_Complex_list = Unit_Complex_list[['unit.id', 'unit.url', 'complex.name', 'capacity_Tons', 'under_construction_Tons']]

    return Unit_Complex_list      