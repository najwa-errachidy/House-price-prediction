# import libraries
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd

# helper functions
def checkStanding(data):
    icon = data.find('i', {'class':'icon-award bigIcon darkblue padB20'})
    if icon:
    	return data.find('p', {'class':'immoBadge'}).get_text()
    return None

def checkConstruction(data):
    icon = data.find('i', {'class':'icon-wrench bigIcon darkblue padB20'})
    if icon:
        return data.find('p', {'class':'immoBadge'}).get_text()
    return None

def checkLivraison(data):
    icon = data.find('i', {'class':'icon-key bigIcon darkblue padB20'})
    if icon:
        return data.find('p', {'class':'immoBadge'}).get_text()
    return None

# preparing dataframe
column_names = ["anouncer", "ResName", "price","location","standing","construction","Delivery"]
df = pd.DataFrame()

# specify the url 
url = 'https://www.mubawab.ma/fr/listing-promotion'

# run firefox webdriver from executable path of your choice
driver = webdriver.Firefox(executable_path =r'/Users/najwaerrachidy/downloads/geckodriver')

# get web page
driver.get(url)
time.sleep(10)
soup = BeautifulSoup(driver.page_source)

# get number of pages
pages = soup.find('span', {'id':'lastPageSpan'}).get_text()

# pagination
pageList = ['https://www.mubawab.ma/fr/listing-promotion:p:'+str(i) for i in range(1,int(pages))]

for page in pageList:
	driver.get(page)
	soup1 = BeautifulSoup(driver.page_source)
	l = []
	for x in soup.findAll('li', {'class':'promotionListing listingBox w100'}):
		l.append(x.get('linkref'))
	for site in l:
		df1 = {"anouncer":'' , "ResName": '', "price": '',"location": '',"standing": '',"construction": '',"Delivery":''}
		driver.get(site)
		soup1 = BeautifulSoup(driver.page_source)

		#collecting price
		for data in soup1.findAll('div',{'promotionInfoBox col-3'}):
			price = data.find('h2').get_text().replace('À partir de','')
			price = price.replace(' ','').replace('\t','').replace('\n','').replace('DH','')
			if price == 'Prixàconsulter':
				df1['price'] = None
			else:
				df1['price'] = price

		#collecting anouncer
		for data in soup1.findAll('p',{'class':'link'}):
			anouncer = data.find('a').get_text().replace('\t','').replace('\n','')
			df1['anouncer'] = anouncer

		#collecting residence name
		for data in soup1.findAll('div',{'promotionInfoBox col-5'}):
			res = data.find('h1').get_text().replace('\t','').replace('\n','')
			df1['ResName'] = res

		#collecting type 
		div_data = soup1.findAll('div',{'class':'promotionInfoBox lHeight1 col-1 centered'})
		result = [None] * 3
		res = [None] * 3
		for data in div_data:
			if checkStanding(data) != None:
				result[0] = checkStanding(data).replace('\t','').replace('\n','')
			if checkConstruction(data) != None:
				result[1] = checkConstruction(data).replace('\t','').replace('\n','')
			if checkLivraison(data) != None:
				result[2] = checkLivraison(data).replace('\t','').replace('\n','').replace('Livraison','')

		df1['standing'] = result[0]
		df1['construction'] = result[1]
		df1['Delivery'] = result[2]

		#collecting location
		for data in soup1.findAll('div',{'promotionInfoBox col-5'}):
			loc = data.find('span').get_text().replace('\t','').replace('\n','')
			df1['location'] = loc

		df = df.append(df1, ignore_index = True)
		print(df)

# store the dataframe as csv file
df.to_scv('outData.scv')