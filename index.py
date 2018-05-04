from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


path_to_chromedriver = '/Users/michaelroker/Projects/chromedriver'

browser = webdriver.Chrome(executable_path = path_to_chromedriver)

url = 'http://www.bahamasrealty.bs'


browser.get(url)

# select the island
select = Select(browser.find_element_by_name('island'))
select.select_by_visible_text("Nassau/New Providence")

#select sale or rent
select = Select(browser.find_element_by_name('category2'))
select.select_by_visible_text('For Rent')


select = Select(browser.find_element_by_name('property_type'))
select.select_by_visible_text('Apartment')

#click submit
browser.find_element_by_xpath('//*[@id="quicksearch"]/form/input[4]').click()


#create function to scrape data from page

links = []
description = []
location = []
prices = []

def scrape_data():
    """
    This function dumps data into the the funtion 'mydata', and loops through resultitems
    and add descriptions, titles, prices, and links to lists.
    """
    mydata = browser.page_source

    soup = BeautifulSoup(mydata, 'html.parser')

    resultItem = soup.find_all(class_="resultItem")


    for result in resultItem:
        links.append(result.a)
        print('Links have been added to list...')

        if result.find(class_='proptype'):
            description.append(result.find(class_='proptype').contents[0])
            print('description appended...')

        if result.find(class_='location'):
            location.append(result.find(class_='location').contents[0])
            print('location has been appended...')

        if result.find(class_='price'):
            prices.append(result.find(class_='price').contents[0])
            print('price list appended...')


while True:
    scrape_data()
    try:
        browser.find_element_by_id('nextpage').click()
    except Exception as e:
        break




# build a dataframe, export to CSV
d = {'Links': links, 'Descriptions': description, 'Location': location, 'Price': prices}
df = pd.DataFrame(data = d)

df.to_csv('BahamasRealty.csv')

# close browser
browser.close()







