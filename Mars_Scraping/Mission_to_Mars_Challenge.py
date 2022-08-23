#!/usr/bin/env python
# coding: utf-8

# Article Scraping
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

#set executable path
executable_path = {'executable_path': ChromeDriverManager().install()}

#set up URL for scraping
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

#set up html parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p



# ## Featured Images
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()

df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df

df.to_html()



# D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# Hemispheres

# 1. Use browser to visit the URL 
url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

browser.visit(url)

# 2a. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
# 3a. get the list of all hemispheres
links = browser.find_by_css('a.product-item h3')

# 3b. loop through the links, click link, find sample anchor return href
for index in range(len(links)):
    hemispheres = {}
    
    # 3c. find elements on each loop (avoids a stale element excception)
    browser.find_by_css('a.product-item h3')[index].click()

    # 3d. find sample IMAGE anchor tag, extract href
    sample_element = browser.links.find_by_text("Sample").first
#     sample_element = browser.find_element("Sample").first
    hemispheres["img_url"] = sample_element["href"]
    
    #3e. get hemisphere TITLE
    hemispheres["title"] = browser.find_by_css("h2.title").text
    
    #3f. Append dictionary with image and title
    hemisphere_image_urls.append(hemispheres)
    
    #3g. navigate backwards
    browser.back()

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

browser.quit() 

