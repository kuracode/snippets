from bs4 import BeautifulSoup
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import time

service = Service(executable_path='./geckodriver.exe')
options = webdriver.FirefoxOptions()
options.add_argument('-headless')

url = "https://www.foreca.fi/Finland/Kokkola/details"
driver = webdriver.Firefox(service=service, options=options)
driver.get(url)
time.sleep(5)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

temps = soup.find_all('div', {'class': 't warm'})
klos = soup.find_all('div', {'class': 'h'})
descs = soup.find_all('div', {'class': 'wx'})

time_list = []
temperature_list = []
description_list = []

for klo in klos[1:]:
    time_list.append(klo.text)

for temp in temps:
    temperature_list.append(temp.text)

for desc in descs:
    description_list.append(desc.text)

weather_details = {time_list[i]: (temperature_list[i], description_list[i]) for i in range(len(time_list))}

for time, (warmth, description) in weather_details.items():
    print(f"{time}, {warmth}, {description}")

driver.close()