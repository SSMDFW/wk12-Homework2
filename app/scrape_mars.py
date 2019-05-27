from flask import Flask, render_template
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
import datetime as  dt
import time
import numpy as np
from selenium import webdriver
app = Flask(__name__)
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Use database and create it
# db = client.mars_dbc
# collection = db.mars_data_entries


# def init_browser():
#     executable_path = {"executable_path": "C:\\Users\\silva\\Desktop\\chromedriver"}
#     return Browser("chrome", **executable_path)

def scrape_mars ():
    """Scrapes various websites for information about Mars, and returns data in a dictionary"""
    browser = Browser("chrome", executable_path="C:\\Users\\silva\\Desktop\\chromedriver", headless=True)
    news_title, news_p= mars_news(browser)

    ddata = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_image(browser),
        "hemispheres": hemispheres(browser),
        "weather": twitter_weather(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
        }

    # Stop webdriver and return data
    browser.quit()
    return ddata



def mars_news(browser):
    # NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'lxml')
    try:
        news_list = soup.find('ul', class_='item_list')
        first_item = news_list.find('li', class_='slide')
        news_title = first_item.find('div', class_='content_title').text
        news_p = first_item.find('div', class_='article_teaser_body').text
        # mars_dataI["news_title"] = news_title
        # mars_dataI["news_p"] = news_p
    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):
   #JPL Mars Space Images - Featured Image

    urlj = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(urlj)
    time.sleep(1)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1) 

    expand = browser.find_by_css('a.fancybox-expand')
    expand.click()
    time.sleep(1)

    htmlj = browser.html
    j_soup = bs(htmlj, 'lxml')
    try:
        img_relative = j_soup.find('img', class_='fancybox-image')['src']
        featured_image_url = 'https://www.jpl.nasa.gov'+img_relative
        # mars_dataI["featured_image_url"] =featured_image_url

    except AttributeError:
        return None
    return featured_image_url

def twitter_weather(browser):       
    #Mars Weather

    urlw = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(urlw)
    time.sleep(1)
    htmlw = browser.html
    w_soup = bs(htmlw, 'lxml')

    tweets = w_soup.find('ol', class_='stream-items')
    mars_weather = tweets.find('p', class_="tweet-text").text
    # mars_dataI["mars_weather"] = mars_weather
    return mars_weather
    
def mars_facts(browser):    

    #Mars Facts
    urlf = 'https://space-facts.com/mars/'
    browser.visit(urlf)
    time.sleep(1)
    htmlf = browser.html
    facts_soup = bs(htmlf, 'lxml')
    try:
        fact_table = facts_soup.find('table', class_='tablepress tablepress-id-mars')
        col1 = fact_table.find_all('td', class_='column-1')
        col2 = fact_table.find_all('td', class_='column-2')
    except BaseException:
        return None
    measures = []
    values = []

    for row in col1:
         measure = row.text.strip()
         measures.append(measure)
            
    for row in col2:
        value = row.text.strip()
        values.append(value)
            
    mars_facts = pd.DataFrame({
        "Measure":measures,
        "Value":values
        })


    return  mars_facts.to_html(classes ="table table-striped")
        
def hemispheres(browser):
    # Mars Hemispheres
    mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemis = []
    browser.visit(mars_hemisphere_url)
    
    for i in range(1,9,2):
        
        d_links = browser.find_by_css('a.product-item')
        d_links[i].click()
        time.sleep(1)
        hemi_data = hemi_scrape(browser.html)

        # Append hemisphere object to list
        hemis.append(hemi_data)
        browser.back()
    return(hemis)
def hemi_scrape(html_text):
    # Mars Hemispheres
    hem_soup = bs(html_text, 'lxml')
    try:
        hem_title = hem_soup.find("h2", class_="title").get_text()
        hem_sample = hem_soup.find("a",  text="Sample").get("href")
    except AttributeError:
        hem_title = None
        hem_sample = None    
        
    hemisII = {
        "title": hem_title,
        "img_url": hem_sample
     }

    return hemisII


if __name__ == "__main__":

    print(scrape_mars())