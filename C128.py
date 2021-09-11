from selenium import webdriver
from bs4 import BeautifulSoup, element
import time
import csv
import requests
url = 'https://exoplanets.nasa.gov/discovery/exoplanet-catalog/'
browser = webdriver.Chrome('c:/bin/chromedriver')
browser.get(url)
time.sleep(10)
headers=['name','light_Years_from_earth','planet_mass','stellar_magintude','disovery_date','hyper_link','planet_type','planet_radius','orbital_radius','orbital_period','eccentricity']
planet_data = []
new_planet_data = []
final_data = []
def scrap():
    for i in range(0,452):
        soup = BeautifulSoup(browser.page_source,'html.parser')
        current_page = int(soup.find_all('input',attrs={'class','page_num'})[0].get('value'))
        if current_page<i:
            browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        elif current_page > i:
            browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
        else:
            break
        for ultag in soup.find_all('ul',attrs={'class','exoplanet'}):
            li_tags = ultag.find_all('li')
            temp = []
            for index,li_tag in enumerate(li_tags):
                if index == 0:
                    temp.append(li_tag.find_all('a')[0].contents[0])
                else:
                    try:
                        temp.append(li_tag.contents[0])
                    except:
                        temp.append('')
            hyperlinktag = li_tags[0]
            temp.append('https://exoplanets.nasa.gov'+ hyperlinktag.find_all('a',href = True)[0]['href'])
            planet_data.append(temp)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        print(f"{i} page done" )
def scrapMoreData(hyperlink):
    try:

        page = requests.get(hyperlink)
        soup = BeautifulSoup(browser.page_source,'html.parser')
        temp = []
        for trtag in soup.find_all('tr',attrs ={'class':'fact_row'}):
            tdtags = trtag.find_all('td')
            for tdtag in tdtags:
                try:
                    temp.append(tdtag.find_all('div',attrs={'class':'value'})[0].contents[0])
                except:
                    temp.append('')
        new_planet_data.append(temp)
    except:
        time.sleep(2)
        scrapMoreData(hyperlink)
scrap()
for index,data in enumerate(planet_data):
    scrapMoreData(data[5])
for index,data in enumerate(planet_data):
   new = new_planet_data[index]
   final_data.append(data+new)
   #   final_data.append(data+final_data[index])
with open('data.csv','w')as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(final_data)
##//*[@id="results"]/ul[3]/li[1]/a