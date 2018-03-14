from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
from splinter import Browser
import pandas as pd
import tweepy
import re

def scrape():
    #NASA FEATURED NEWS
    #retrieve base html
    url = 'https://mars.nasa.gov/news/'
    browser = Browser('chrome', headless=False)
    browser.visit(url)
    news_soup = bs(browser.html, "html5lib") #lxml stopped working in new env

    #find first article
    article_soup = news_soup.find('div', class_ = 'list_text')

    #subsearch title and text from within article to make sure that they match
    news_title = article_soup.find('div', class_ = 'content_title').text
    #cleanup
    news_title = news_title.replace('\n','')

    news_p = article_soup.find('div', class_ = 'article_teaser_body').text

    #JPL FEATURED IMAGE
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    image_soup = bs(browser.html, 'html5lib')
    image_url = image_soup.find(class_ = 'carousel_item')['style']

    featured_image_url = 'https://www.jpl.nasa.gov/' + image_url.split("'")[1]

    #MARS FACTS
    url = 'https://space-facts.com/mars/'
    dfs = pd.read_html(url)
    df = dfs[0]
    df = df.rename(columns = {0: 'Mars Data', 1:''})
    df = df.set_index('Mars Data')
    table_html = df.to_html()
    table_html = table_html.replace('dataframe', '')
    table_html = table_html.replace('<th></th>', ' ')

    border_pat = re.compile(r'border="."') #just for fun and a little formatting
    class_pat = re.compile(r'class=""')
    table_html = table_html.replace(border_pat.search(table_html).group(), '')
    table_html = table_html.replace(class_pat.search(table_html).group(), '')
    table_html
    '''url = 'https://space-facts.com/mars/'
    dfs = pd.read_html(url)
    df = dfs[0]
    df = df.rename(columns = {0:'Mars Data', 1:' '})
    df = df.set_index('Mars Data')
    table_html = df.to_html()'''

    #MARS WEATHER
    url = "https://twitter.com/marswxreport"
    browser.visit(url)
    twit_soup = bs(browser.html, 'html5lib')
    tweets_html = twit_soup.findAll(class_ = "js-tweet-text-container")
    
        #can give extended forecast
    weather = []
    for tweet in tweets_html:
        text = tweet.find('p').text
        if 'sol' in text.lower() and 'low' in text.lower():
            weather.append(text)
            #text.split(' ')[1]
    mars_weather = weather[0]
    mars_weather


    #HEMISPHERE IMAGES
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    hemispheres_soup = bs(browser.html, 'html5lib').find_all(class_ = 'item')

    base_url = 'https://astrogeology.usgs.gov'
    hemisphere_imgs = {}
    for hsoup in hemispheres_soup:
        sub_url = hsoup.find('a')['href']
        browser.visit(base_url + sub_url)
        soup = bs(browser.html, 'html5lib')
        for href in soup.find_all('a'):
            if 'full.jpg' in href['href']:
                print(href['href'])
                hemisphere = href['href'].split('Viking/')[1] .split('/')[0].replace('_enhanced.tif','')
                hemisphere_imgs[hemisphere] = href['href']

    # return results of each section in a single dictionary
    return {'news_title': news_title,
            'news_p': news_p,
            'featured_image_url': featured_image_url,
            'table_html': table_html,
            'hemisphere_imgs': hemisphere_imgs,
            'weather': mars_weather
           }
            
            
            