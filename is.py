from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import time

service = Service(executable_path='./geckodriver.exe')
options = webdriver.FirefoxOptions()
options.add_argument('-headless')

url = "https://www.is.fi"
driver = webdriver.Firefox(service=service, options=options)
driver.get(url)
time.sleep(5)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

temps = soup.find_all('li', {'class': 'generic-list-item padding-y-16'})

for temp in temps:
    # Find the anchor tag within the 'li' element
    anchor_tag = temp.find('a')
    if anchor_tag:
        # Extract the link URL from the 'href' attribute
        link_url = anchor_tag.get('href')
        print("Otsikko:", temp.text)
        print("Linkki:", url + link_url)
        print("-" * 100)
        
        # Open the link in a new tab or window
        driver.execute_script("window.open('{}', '_blank');".format(url + link_url))
        time.sleep(5)  # Wait for the new page to load
        
        # Switch to the newly opened tab or window
        driver.switch_to.window(driver.window_handles[1])
        
        # Perform additional scraping on the newly opened page
        new_page_html = driver.page_source
        new_soup = BeautifulSoup(new_page_html, "html.parser")
        
        contents = new_soup.find_all('p', {'class': 'article-body mb-24 px-16'})
        for content in contents:
            print(content.text)
        
        # Close the newly opened tab or window
        driver.close()
        
        # Switch back to the original tab or window
        driver.switch_to.window(driver.window_handles[0])
        
        print()  # Add a newline for better readability between iterations

driver.close()

