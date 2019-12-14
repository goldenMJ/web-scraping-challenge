#!/usr/bin/env python
# coding: utf-8



from splinter import Browser
from bs4 import BeautifulSoup
import time
import requests
import pymongo
from selenium import webdriver


# # **Create Database in MongoDB**
# ![title](Images/mongo.png)

# # **Connect to Mongo DB Mars DB**


conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)




# Define database and collection
db = client.mars
collection = db.items


# **Get executable_path**



# # **Step 1 - Scraping**

# **NASA Mars News**
# 
# Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.




def latest_nasa_news():
    mars_news_data = []
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    #need timer to ensure page has load before scraping?
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # data structures
    posting = {}
    titles = []
    content = []   
    
    title_results = soup.find_all("div", {"class": "content_title"})
    teaser_results = soup.find_all("div", {"class": "article_teaser_body"})

    for result in title_results:
        title = result.find('a').text
        titles.append(title)

    for teaser in teaser_results:
        b = teaser.get_text()
        content.append(b)
    # not all 'content_title' tags have 'article_teaser_body' content
    # loop through all content, ignoring 'content_title without data'
    a = (min( len(titles), len(content) ))
    #print (a)
    
    for i in range(1):
        posting = {'title': titles[i], 'text': content[i]}
        mars_news_data.append(posting)
        #coll.insert_one(posting)
        
    return mars_news_data


# **JPL Mars Space Images - Featured Image**
# 
# Latest Mars image



def latest_mars_image():
    url_mars = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url_mars)
    #need timer to ensure page has load before scraping?
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image = soup.find("a", {"class": "button fancybox"})
    med_size = image.attrs['data-fancybox-href']
    large_size = med_size.replace('mediumsize', 'largesize')
    large_size = large_size.replace('_ip', '_hires')
    images_link = 'https://www.jpl.nasa.gov' + large_size
    
    return images_link
    


# **Twitter Latest Mars Weather**



def latest_mars_weather():
    url_mars_weather = "https://twitter.com/marswxreport?lang=en"
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url_mars_weather)
    #need timer to ensure page has load before scraping?
    time.sleep(5)
    soup = BeautifulSoup(browser.html, 'html.parser')   
    weather_container = soup.find("p", {"class": "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"})
    forecast = weather_container.text
    wc = weather_container.find('a').text
    
    wetter = forecast.replace(weather_container.find('a').text, '')
    
    return wetter
    


# **Mars Table Facts**



def mars_facts():
   mars_facts_url = 'https://space-facts.com/mars/'
   import pandas as pd
   
   #browser = Browser()
   executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
   browser = Browser('chrome', **executable_path, headless=False)
   
   browser.visit(mars_facts_url)
   time.sleep(5)
   html = browser.html
   soup = BeautifulSoup(html, 'html.parser')
   
   mars_facts_table = soup.find("table", {"class": "tablepress tablepress-id-p-mars"})
   df_mars_facts = pd.read_html(str(mars_facts_table))

   html_table = df_mars_facts
   
   return df_mars_facts
   
   
   


# **Mars Hemispheres**
# 
# Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
# 
# 
# You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
# 
# 
# Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
# 
# 
# Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.



def mars_image_url():
    img_url = []
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    #need a pause to ensure page has load before scraping?
    time.sleep(7)
    soup = BeautifulSoup(browser.html, 'html.parser')
    astrogeology_items = soup.find_all("div", {"class": "description"})
    img_url = []
    for astro in astrogeology_items:
        rel_link = astro.find('a')
        img_url.append(rel_link.attrs['href'])
    
    return(img_url)
    




def mars_hemispheres(url, hemispheres_list):
    hemi_dict = {}
    base_asrogeology_url = 'https://astrogeology.usgs.gov'
    astro_url = base_asrogeology_url + url
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(astro_url)
    hemi_image_urls = {}

    time.sleep(8)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    link_section = soup.find_all("section", {"class": "block metadata"})
    for section in link_section:
        print(section.find('h2').text)
        alink = section.find('a')
        print(alink.attrs['href'])
        hemi_dict['title'] = section.find('h2').text
        hemi_dict['img_url'] = alink.attrs['href']
        hemispheres_list.append(hemi_dict)

    
    return hemispheres_list




def scraper_data():
    mars_scraper = {}
    
    mars_news_list = []
    hemi_image_urls = []
    
    featured_image_url = latest_mars_image()
    mars_weather_string = latest_mars_weather()
    mars_news_list = latest_nasa_news()
    mars_facts_df = mars_facts()
    
    astrogeology_relative_links = mars_image_url()
    for astro in astrogeology_relative_links:
        hemi_image_urls = mars_hemispheres(astro, hemi_image_urls)
    

    
    mars_scraper['news_title'] = mars_news_list[0]['title']
    print 
    mars_scraper['news_p'] = mars_news_list[0]['text']
    mars_scraper['featured_image_url'] = featured_image_url
    mars_scraper['mars_weather'] = mars_weather_string
    mars_scraper['mars_df'] = str(mars_facts_df)
    mars_scraper['hemisphere_image_urls'] = hemi_image_urls
    
    
    
    return mars_scraper
    
    








