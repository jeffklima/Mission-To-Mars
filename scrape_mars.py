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
    executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

# Create Mission to Mars dictionary
def scrape_info():

    # Initialize browser 
    browser = init_browser()
    news_title, news_p = scrape_mars_news()

    mars_data = {
        'news_title': news_title,
        'news_paragraph': news_p,
        'featured_img_url': scrape_mars_image(),
        'mars_weather_tweet': scrape_mars_weather(),
        'facts': scrape_mars_facts(),
        'hemisphere_image_urls': scrape_mars_hemispheres()
        }

    browser.quit()

    return mars_data   

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
        
    browser.quit()
        
    return news_title, news_p
    

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
    featured_image_url = site_url + featured_img_url
    browser.quit()   

    return featured_image_url

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
        
    browser.quit()

    return mars_weather_tweet

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

    browser.quit()

    return facts

# MARS Hemispheres
def scrape_mars_hemispheres():

    # Initialize browser 
    browser = init_browser()

    # Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    hemispheres_html = browser.html

    soup = BeautifulSoup(hemispheres_html, 'html.parser')

    hemis = soup.find_all('div', class_='item')

    hemisphere_image_urls = []

    hemispheres_main = 'https://astrogeology.usgs.gov'

    # Loop through to get each image title and url
    for i in hemis: 
        title = i.find('h3').text

        end_of_url = i.find('a', class_='itemLink product-item')['href']
        
        browser.visit(hemispheres_main + end_of_url)
        
        img_name = browser.html
        
        soup = BeautifulSoup(img_name, 'html.parser')
        
        img_url = hemispheres_main + soup.find('img', class_='wide-image')['src']
        
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})


    browser.quit()

    return hemisphere_image_urls