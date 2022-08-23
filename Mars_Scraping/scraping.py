## Article Scraping

# Import Splinter and BeautifulSoup
from inspect import Attribute
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True) #true do not need to see browser being scraped

    #set news title and paragraph varibles
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
        
    }

    # Stop webdriver and return data
    browser.quit()
    return data



# Scrape Mars News
def mars_news(browser): #browser = argument; use browser varible defined outside of function
 
    # Visit the mars nasa browsernews site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #set up html parser;Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
   
    except AttributeError:
        return None, None

        #Instead of having our title and paragraph printed within the function, return them from the function so they can be used outside of it
    return news_title, news_p


#  Scrape Featured Images
def featured_image(browser): #declare and define function
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url


 # Scrape Mars Facts
def mars_facts(): #define function
    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
      return None

    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
       

    #convert to html, add bootstrap
    return df.to_html()

# Challenge part 2: append dictionaries from part 1 to the scraping app
def hemispheres(browser):
     #1. Use browser to visit the URL 
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    # 2a. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    # 3a. get the list of all hemispheres
    links = browser.find_by_css('a.product-item h3')

    # 3b. loop through the links, click link, find sample anchor return href
    for index in range(len(links)):
        
        # 3c. find elements on each loop (avoids a stale element excception)
        browser.find_by_css('a.product-item h3')[index].click()
        hemisphere_data = scrape_hemisphere(browser.html)
        hemisphere_image_urls.append(hemisphere_data)
        #3g. navigate backwards
        browser.back()

    return hemisphere_image_urls

def scrape_hemisphere(html_text):
    #parse html text
    hemisphere_soup = soup(html_text, "html.parser")

    try:
        title_element = hemisphere_soup.find("h2", class_="title").get_text()
        sample_element = hemisphere_soup.find("a", text="Sample").get("href")
    except AttributeError:
        title_element = None
        sample_element = None
    hemispheres_dictionary = {
        "title": title_element,
        "img_url": sample_element
    }
    return hemispheres_dictionary


# tell flask script is complete and ready for use
if __name__ == "__main__":
    
    # If running as script, print scraped data
    print(scrape_all())




