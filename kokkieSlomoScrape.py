# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 14:11:27 2018

@author: Thomas
"""
from datetime import datetime
startTime = datetime.now()

# Load packages 
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pandas as pd

# Define functions
def getPageNumber(articleUrl):
    html = urlopen(articleUrl)
    bsObj = BeautifulSoup(html.read(), "html5lib")
    for span in bsObj.findAll("span", {"class":"pages"}):
        pages = span.get_text()
        pageNumber = int(pages.split("of ")[1])
    return pageNumber

def getPostListings(articleUrl, pageNumber):
    postListings = [articleUrl]
    for x in range(2, pageNumber + 1):
        newUrl = (articleUrl + "page/" + str(x) + "/")
        postListings.append(newUrl)
    return postListings

def getLinks(articleUrl):
    html = urlopen(articleUrl)
    time.sleep(5)
    bsObj = BeautifulSoup(html.read(), "html5lib")
    internalList = []
    for h2 in bsObj.findAll("h2", {"class":"post-box-title"}):
        a = h2.find('a', attrs={'href': re.compile("^http://")})
        internalList.append(a.attrs['href'])
    return internalList

def makeFinal(x):
    html = urlopen(x)
    time.sleep(5)
    bsObj = BeautifulSoup(html.read(), "html5lib")
    title = bsObj.find("h1")
    for h1 in title:
        internaldf = pd.DataFrame({'Title': [title.get_text()], 'Link': [x]})
    return internaldf

# Execute
pageNumber = getPageNumber("http://www.kokkieslomo.nl/category/kokkies-recepten/")
time.sleep(5)
listings = getPostListings("http://www.kokkieslomo.nl/category/kokkies-recepten/", pageNumber )
recipeUrls = []
for link in listings:
    recipeUrls.extend(getLinks(link))
             
recipeBook = pd.DataFrame(columns=['Title','Link'])
for item in recipeUrls:
    recipeBook = recipeBook.append(makeFinal(item), ignore_index = True, sort = True)

recipeBook.to_csv("files/Kokkie_Slomo_All_Recipes.csv")

print(datetime.now() - startTime)
