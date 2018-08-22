# -*- coding: utf-8 -*-
import requests
import html5lib
from bs4 import BeautifulSoup
import csv
import datetime


class fuel_crawler:
	def crawlsite_and_writetocsv(self):
		print "Gathering fuel prices ..."
		URL = "https://www.mypetrolprice.com/Petrol-price-in-india.aspx"
		response = requests.get(URL)
		soup = BeautifulSoup(response.content, 'html5lib')
		states = soup.findAll("h2", {"class" : "txtC"})
		print "Preparing your csv ..."
		file_name = 'fuel_prices_'+str(datetime.datetime.now().strftime("%Y-%m-%d"))
		with open(str(file_name)+'.csv', 'w+') as csvfile:
			csvfile.write('State, City, Price, Deviation, Date\n')
			for one_state in states:
				state_name = one_state.a.string
				#print "state = {}".format(state_name)
				#print ("-------------")
				#print "FULL"
				#print one_state
				#$print "next state"
				divs =  one_state.find_next_sibling()
				#print divs
				cities = divs.findAll("div" , {"id" : "mainDiv"})
				for one_city in cities:
					#print ("printing cities now ----------------------")
					city_name = one_city.a['title']
					#print "City = {}".format(city_name)
					price = one_city.b.string
					new_price = price.encode('ascii', 'ignore').decode('ascii')
					#print "Price = {}"
					#print price, new_price
					date_field = one_city.find("div", {"class" : "displayInlineBlock boderBox" })
					date_value = date_field.string.strip()
					#print "date_value = {}".format(date_value)
					deviation = one_city.span.string
					#print "deviation = {}".format(deviation)
					csv_str = '{},{},{},{},{}\n'.format(state_name,city_name,new_price,deviation, date_value)
					csvfile.write(csv_str)
		print "Please find today's fuel prices in the file {}.csv located in the current directory".format(file_name)

if __name__ == "__main__":
    fuel_crawler().crawlsite_and_writetocsv()