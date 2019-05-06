
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser

import time
import numpy as np
from selenium import webdriver




def init_browser():
    executable_path = {"executable_path": "C:\\Users\\silva\\Desktop\\chromedriver"}
    return Browser("chrome", **executable_path)

def scrape ():
    """Scrapes various websites for information about Mars, and returns data in a dictionary"""
    
    browser = init_browser()
    mars_data = {}

    # NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'lxml')

    news_list = soup.find('ul', class_='item_list')
    first_item = news_list.find('li', class_='slide')
    news_title = first_item.find('div', class_='content_title').text
    news_p = first_item.find('div', class_='article_teaser_body').text
    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p

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

    img_relative = j_soup.find('img', class_='fancybox-image')['src']
    featured_image_url = 'https://www.jpl.nasa.gov'+img_relative
    mars_data["featured_image_url"] =featured_image_url

        
    #Mars Weather

    urlw = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(urlw)
    time.sleep(1)
    htmlw = browser.html
    w_soup = bs(htmlw, 'lxml')

    tweets = w_soup.find('ol', class_='stream-items')
    mars_weather = tweets.find('p', class_="tweet-text").text
    mars_data["mars_weather"] = mars_weather

    #Mars Facts
    urlf = 'https://space-facts.com/mars/'
    browser.visit(urlf)
    time.sleep(1)
    htmlf = browser.html
    facts_soup = bs(htmlf, 'lxml')

    fact_table = facts_soup.find('table', class_='tablepress tablepress-id-mars')
    col1 = fact_table.find_all('td', class_='column-1')
    col2 = fact_table.find_all('td', class_='column-2')

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

    htmlf = mars_facts.to_html(header=False, index=False)
    mars_data["mars_facts_t"] = mars_facts

    # Mars Hemispheres
    mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemis = []

    for i in range(1,9,2):
        hemi = {}
        
        browser.visit(mars_hemisphere_url)
        time.sleep(1)
        hem_html = browser.html
        hem_soup = bs(hem_html, 'lxml')
        hem_links = hem_soup.find_all('a', class_='product-item')
        hem_name = hem_links[i].text.strip('Enhanced')
        
        d_links = browser.find_by_css('a.product-item')
        d_links[i].click()
        time.sleep(1)
        browser.find_link_by_text('Sample').first.click()
        time.sleep(1)
        browser.windows.current = browser.windows[-1]
        hem_img_html = browser.html
        browser.windows.current = browser.windows[0]
        browser.windows[-1].close()
        
        hem_img_soup = bs(hem_img_html, 'lxml')
        hem_img_path = hem_img_soup.find('img')['src']

    
        hemi['title'] = hem_name.strip()
        hemi['img_url'] = hem_img_path
        hemis.append(hemi)

    mars_data["hemisphere_images"] = hemis

    #browser.quit()

    return(mars_data)