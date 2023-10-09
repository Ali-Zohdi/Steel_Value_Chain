from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time


url = 'https://infosaba.com'
s = Service(r"Z:\\HQ\BDM\\a.zohdi\\Data Engineering\\Github\\Geocoding\\chromedriver-win32\\chromedriver-win32\\chromedriver.exe")

driver = webdriver.Chrome(service=s)
driver.get(url)
driver.set_window_size(1920, 1080)

i = 1
industries = []
while i > 0:
    mother_industry = driver.find_element(By.XPATH, f'//*[@id="mainPageContainer"]/div[2]/div[2]/div[{i}]/a/div/div')
    industry = mother_industry.text.split('\n')

    mother_industry.click()

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    sub_industries = soup.find_all(class_='d-flex m-1')

    print(driver.current_url)
    sub_ind = 0
    while sub_ind in range(len(sub_industries)):
        sub_ind += 1

        time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sub_industry = driver.find_element(By.XPATH, f'//*[@id="mainPageContainer"]/div/div[2]/div/a[{sub_ind}]')
        url = sub_industry.get_attribute('href')

        ind = sub_industries[sub_ind - 1].find('h3').text.strip()

        industries.append([industry[0], industry[1], ind, url])
        print(industries)

    driver.back()
    i += 1

print(industries)