
# Import BeautifulSoup
from bs4 import BeautifulSoup
import requests
import pandas as pd
from splinter import Browser


executable_path = {"executable_path": r"C:/Users/kouam/Desktop/chromedriver.exe"}
browser = Browser("chrome", **executable_path, headless=False)



def scrape():
 
    mars_dict = {}
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')

    # Collecting the latest News Title and Paragragh Text
    news_title = soup.find('div', class_="content_title").text
    news_p = soup.find('div', class_="rollover_description_inner").text

    #print(news_title)
    #print(news_p)
    mars_dict['news_title'] = news_title
    mars_dict['news_p'] = news_p


    # JPL Mars Space Images - Featured Image
    url_mars = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_mars)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve page with the requests module
    response_mars = requests.get(url_mars)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup_mars = BeautifulSoup(response_mars.text, 'html.parser')

    # Find the image url for the current Featured Mars Image
    img_url = soup_mars.find('div', class_='carousel_items')
    
    url_style = img_url.find('article')['style']
    url_style = url_style.replace('background-image: url(', '').replace(');', '')
  
    featured_image_url = "https://www.jpl.nasa.gov" 
    featured_image_url = featured_image_url + url_style
    featured_image_url = featured_image_url.replace("'", '')

    #print(featured_image_url)
    mars_dict['featured_image_url'] = featured_image_url



    # MARS WEATHER

    url_marsweather = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_marsweather)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # Retrieve page with the requests module
    response_marsweather = requests.get(url_marsweather)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup_marsweather = BeautifulSoup(response_marsweather.text, 'html.parser')

    #Find the most recent tweet
    recent_tweet = soup_marsweather.find('div', class_='js-tweet-text-container')
    mars_weather = recent_tweet.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    #print(mars_weather)
    mars_dict['mars_weather'] = mars_weather



    # MARS FACTS

    url_marsfacts = 'https://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    ### BEGIN SOLUTION
    tables = pd.read_html(url_marsfacts)
    tables

    df = tables[0]
    df.columns = ['Facts', 'Values']
    df.head()
    mars_facts = df.to_html
    mars_dict['mars_facts'] = mars_facts


    # MARS HEMISPHERES

    url_marshemis = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_marshemis)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve page with the requests module
    response_marshemis = requests.get(url_marshemis)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup_marshemis = BeautifulSoup(response_marshemis.text, 'html.parser')

    # Retrieve all elements that contain Mars Hemisphere information
    hemispheres = soup_marshemis.find_all('div', class_='item')

    hemisphere_image_urls = []
    img_url = "https://astrogeology.usgs.gov"
    # Iterate through each hemisphere
    for hemisphere in hemispheres:

        hemis_dict ={}
        hemis_dict['img_url'] = hemisphere.find('img')['src']
        hemis_dict['img_url'] =  hemis_dict['img_url'].replace("'", '')
        hemis_dict['title'] = hemisphere.find('h3').text
    
        hemisphere_image_urls.append(hemis_dict)

    mars_dict['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_dict

