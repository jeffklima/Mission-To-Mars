# Import Dependecies 
from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import requests 

# Initialize browser
def init_browser(): 
    # NOTE: Replace the path with your actual path to the chromedriver

    #Mac Users
    #executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    #return Browser('chrome', **executable_path, headless=False)

    #Windows Users
    exec_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', headless=True, **exec_path)

# Create Mission to Mars global dictionary that can be imported into Mongo
mars_data = {}

# Mars news
def scrape_mars_news():

# Initialize browser 
    browser = init_browser()

    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)

    # HTML Object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve the latest element that contains news title and news paragraph
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    mars_data['news_title'] = news_title
    mars_data['news_paragraph'] = news_p
        
    browser.quit()
        
    return mars_data
    

# FEATURED IMAGE
def scrape_mars_image():

    # Initialize browser 
    browser = init_browser()

    # Use splinter to navigate the site and find the image url for the current Featured Mars Image
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)

    # HTML Object 
    html_image = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_image, 'html.parser')

    site_url = "https://www.jpl.nasa.gov"
    featured_image = soup.find("div", class_="carousel_items").find("article")["style"]
    featured_img_url = featured_image.split("'")[1]
    featured_img_url = site_url + featured_img_url
    featured_img_url 

    # Featured image dictionary
    mars_data['featured_image_url'] = featured_img_url  
            
    browser.quit()   

    return mars_data

# Mars Weather 
def scrape_mars_weather():

    # Initialize browser 
    browser = init_browser()

    # Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page
    mars_weather_url = 'https://twitter.com/MarsWxReport'
    browser.visit(mars_weather_url)

    # HTML Object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    #Latest Tweet
    mars_weather_tweet = soup.find('div', class_='js-tweet-text-container').text

    # Mars weather dictionary
    mars_data['mars_weather_tweet'] = mars_weather_tweet
        
    browser.quit()

    return mars_data 

# Mars Facts
def scrape_mars_facts():

    # Initialize browser 
    browser = init_browser()

    # Visit the Mars Facts webpage and use Pandas to scrape the table containing facts about the planet
    mars_facts_url = 'https://space-facts.com/mars/'

    mars_facts = pd.read_html(mars_facts_url)

    facts_df = mars_facts[1]

    facts_df.columns = ['Description','Value']

    facts_df.set_index('Description', inplace=True)

    facts = facts_df.to_html()

    # Mars facts dictionary
    mars_data['mars_facts'] = facts

    browser.quit()

    return mars_data


# MARS Hemispheres
def scrape_mars_hemispheres():

    # Initialize browser 
    browser = init_browser()

    # Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    hemispheres_html = browser.html

    soup = BeautifulSoup(hemispheres_html, 'html.parser')

    items = soup.find_all('div', class_='item')

    hemisphere_image_urls = []

    hemispheres_url = 'https://astrogeology.usgs.gov'

    # Loop through to get each image title and url
    for i in items: 
        title = i.find('h3').text

        end_of_url = i.find('a', class_='itemLink product-item')['href']
        
        browser.visit(hemispheres_url + end_of_url)
        
        img_name = browser.html
        
        soup = BeautifulSoup(img_name, 'html.parser')
        
        img_url = hemispheres_url + soup.find('img', class_='wide-image')['src']
        
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

    mars_data['hemisphere_image_urls'] = hemisphere_image_urls

    browser.quit()

    return mars_data