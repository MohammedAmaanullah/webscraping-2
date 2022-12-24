
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests
import csv

# NASA Exoplanet URL
START_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"

# Webdriver
browser = webdriver.Edge("C:/Whitehat_jr/PRO-127-130/msedgedriver.exe")
browser.get(START_URL)

time.sleep(10)

planets_data = []

headers = ["star","constellation","right ascension","declination","app. mag.", "Distance","Spectral type","Brown drawf","Mass","Radius","Orbital period","Ecc.","Discovery year"]






def scrap():
    for i in range(0,5):
        while True:
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source,"html.parser")
            current_page_num = int(soup.find_all("input", attrs={"class", "page_num"})[0].get("value"))

            if current_page_num < i:
                browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif current_page_num > i:
                browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else:
                break


        for ul_tag in soup.find_all("ul",attrs={"class":"exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index,li_tags in enumerate(li_tags):
                if(index == 0):
                    temp_list.append(li_tags.find_all("a")[0]).contents[0]
                else:
                    try:
                        temp_list.append(li_tags.contents[0])
                    except:
                        temp_list.append("")



            hyperlink_li_tag = li_tags[0]
            temp_list.append("https://exoplanets.nasa.gov"+ hyperlink_li_tag.find_all("a", href=True)[0]["href"])
            planets_data.append(temp_list)
        browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()

        print(f"Page {i} scraping completed")


        
scrap()


new_star_data=[]
# scrape more data from hyperlink
def scrap_more_date(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content,"html.parser")
        temp_list = []
        for tr_tag in soup.find_all("tr",attrs={"class":"fact_row"}):
            td_tags = tr_tag.find_all("tr")
    
            for td_tag in td_tags:
            
                    try:
                       temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0])
                    except:
                        temp_list.append("")

        new_star_data.append(temp_list)


    except:
        
        time.sleep(1)
        scrap_more_date(hyperlink)

for index, data in enumerate(planets_data):
    scrap_more_date(data[5])

final_star_data = []


for index, data in enumerate(planets_data):
    new_star_data_element = new_star_data[index]
    new_star_data_element = [elem.replace("\n", "") for elem in new_star_data_element]
    new_star_data_element = new_star_data_element[:7]
    final_star_data.append(data + new_star_data_element)



    with open("final.csv","w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(final_planet_data)