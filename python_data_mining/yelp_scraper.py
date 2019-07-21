from selenium import webdriver as web
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time, re, csv, datetime, json

import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.probability import FreqDist

def startYelp(link, restaurant_name):

    #go to the yelp link
    browser = web.Chrome()
    browser.get(url)

    #search the restaurant_name
    

if __name__ == "__main__":
