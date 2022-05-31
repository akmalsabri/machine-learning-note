# import libraries

import urllib
import urllib.request
import bs4 as bs4
import re
import requests
from urllib.error import HTTPError
import nltk

from newspaper import Article
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer 
from nltk.tokenize import word_tokenize 
#from list_symbols import *
import pandas as pd 
import time
import json
from datetime import datetime , date 
import pymongo
from pymongo import MongoClient

nltk.download('wordnet')
nltk.download('punkt')
lemmatizer = WordNetLemmatizer() 



# Create news's project Database

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["News_Project"]

# Create news collection , new's today

collection = mydb.news_today_v1

count = 0

condition = True

while condition :

    page = str(count)

    url_main = 'https://www.theedgemarkets.com/categories/corporate?page='+page
    print(url_main)

    count += 1

    headers = {'User-Agent' : 'Mozilla 5.10'}
    request = urllib.request.Request(url_main, None, headers)
    response = urllib.request.urlopen(request)
    soup = bs4.BeautifulSoup(response,'html.parser')

    time.sleep(2)

    links_ = soup.find_all("div", class_= "addthis_toolbox addthis_default_style addthis_32x32_style listing")

    link_main_page = []

    time.sleep(5)


    for i in links_:
        
        link_1 = i.get('addthis:url')
        print("lalu tak")
        link_main_page.append(link_1)


    for link in link_main_page :

        time.sleep(5)

        url_nltk = link

        article = Article(url_nltk, language="en") 
        article.download() 
        article.parse() 
        article.nlp()


        news_date_dt = article.publish_date
        print(news_date_dt)
        news_title = article.title

        # check if news date is today

        if news_date_dt.date() == date.today():

            print ("Today's news !")

            # readable date in str , iSaham format

            date_str = str(news_date_dt.strftime('%d-%b-%Y %H:%M'))

            # save title and date as dictionary

            ''' Next step insert to pymongo '''


            dict_to_pymongo = {

                "Title": news_title ,
                "Date" : news_date_dt,
                "Date str" : date_str

            }

            print(dict_to_pymongo)

            values_dict = collection.insert_one(dict_to_pymongo).inserted_id
        
        else:

            print("not today..")
            print(news_date_dt.date())
            condition = False

            break



