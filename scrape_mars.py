import pymongo
import datetime
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time
import pandas as pd
import re

def scrape_info():
    mars = {}


    browser = Browser('chrome')
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)


    html = browser.html
    soup = bs(html, "html.parser")
    result = soup.find_all("div", class_= "content_title")
    news_title = result[1].a.text


    html = browser.html
    soup = bs(html, "html.parser")
    result = soup.find("div", class_= "article_teaser_body")
    news_paragraph = result.text
    mars["news_title"] = news_title
    mars["news_paragraph"] = news_paragraph
    mars


    browser = Browser('chrome')
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    browser.find_by_id("full_image").click()
    time.sleep(2)
    browser.links.find_by_partial_text("more info").click()
    html = browser.html
    soup = bs(html, "html.parser")
    result = soup.find("figure", class_= "lede")
    link ="https://www.jpl.nasa.gov" + result.a.img["src"]
    mars["featured_image_url"] = link

    mars


    browser = Browser('chrome')
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    time.sleep(3)
    html = browser.html
    soup = bs(html, "html.parser")
    text_weather = re.compile(r'sol')
    mars_weather = soup.find('span', text = text_weather)
    print(mars_weather.text)
    mars["mars_weather"] = mars_weather.text


    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    tables = tables[0]
    tables.columns = ['description', 'values'] 
    tables = tables.set_index("description")
    html_table = tables.to_html()
    html_table.replace('\n', '')
    mars["facts"] = html_table
    mars


    browser = Browser('chrome')
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    hemisphers_image_url = []
    link = browser.find_by_css("a.product-item h3")
    for x in range(len(link)):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[x].click()
        element=browser.find_link_by_text('Sample').first
        hemisphere['img_url'] = element['href']
        hemisphere['title'] = browser.find_by_css("h2.title").text
        hemisphers_image_url.append(hemisphere)
        browser.back()
    hemisphers_image_url
    mars["hemisphere"] = hemisphers_image_url
    return mars

if __name__ == "__main__":
    print(scrape_info())

