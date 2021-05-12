# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 21:01:40 2017

@author: Elena
"""
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import sys


search_url = 'https://irma.nps.gov/Stats/SSRSReports/Park%20Specific%20Reports/Recreation%20Visitors%20By%20Month%20(1979%20-%20Last%20Calendar%20Year)?Park=MACA'
response = requests.get(search_url).content
parsHtml = BeautifulSoup(response, "lxml")

targets = parsHtml.find_all('tr', attrs={'valign':'top'})
titleTarget = parsHtml.find_all('td', attrs={'style':'WIDTH:235.48mm;min-width: 235.48mm;HEIGHT:7.18mm;'})

titleList= []
for element in titleTarget:
    titleList.append(element.text.encode("ascii","ignore"))
title = titleList[1]

mylist = []
for row in targets:
    myrow = []
    for element in row:
        element = element.text.encode("ascii", "ignore")
        element = element.replace(",","")
        myrow.append(element)
    mylist.append(myrow)
#creates a list of numbers (type: str) without commas

newlist = []
for i in mylist:
    if len(i) == 14:
        newlist.append(i)
#create a list that only has all months, year number, and total visitor column

del newlist[0]
#get rid of first group that was just month names
for group in newlist:
    del group[-1]
#delete the last element, the c6 total visitor column

finallist = [[int(j) if j else 0 for j in i] for i in newlist]
#turn newlist into a list of lists that are integers and empty strings are replaced with 0s

mydict = {i[0]: i[1:] for i in finallist}
#turn into a dictionary where each year is the key

del mylist
del newlist
del finallist

#Ask a user to input a starting and ending year and then tests to ensure the years are in the valid range
userStartYear = int(raw_input("Enter a valid starting year from " + str(min(mydict)) + " - " + str(max(mydict)) + ": "))
userEndYear = int(raw_input("Enter a valid ending year from " + str(min(mydict)) + " - " + str(max(mydict)) + ": "))

if userStartYear < min(mydict) or userEndYear > max(mydict):
    sys.exit("Oh no! You entered the inputs incorrectly and broke the program!")

if userEndYear >= userStartYear:
    myrange = range(userEndYear - userStartYear)
else: 
    sys.exit("Oh  no! You entered the inputs incorrectly and broke the program!")
    
yearsList = [userStartYear + myrange[i] for i in myrange]

compiledList = []
for i in yearsList:
    compiledList.append(mydict[i])

masterList = [instance for i in compiledList for instance in i]
for i in mydict[userEndYear]:
    masterList.append(i)
    
yearsList.append(userEndYear)
yearsList.append(userEndYear + 1)


###################################################################################################
#Create the visualization of the user-selected years from the scraped data.
fig, ax  = plt.subplots()
ax.plot(range(len(masterList)), masterList)

for ax in fig.axes:
    ax.xaxis.set_ticks(range(0, len(masterList), 12))
    ax.xaxis.set_ticks(range(0, len(masterList), 6), minor = True)
    ax.xaxis.set_ticklabels(yearsList, rotation = '45')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_ylim(0, 1.1*max(masterList))
    ax.tick_params(labelsize = 14)

    
for ax in fig.axes:
    ax.yaxis.set_label_text('Visitors',fontsize = 20)
    ax.xaxis.set_label_text('Year', fontsize = 20)

fig.suptitle("Monthly Visitors to " + title + ": " + str(userStartYear) + " - " + str(userEndYear), fontsize = 24)
fig.set_size_inches(12,9)
plt.show()
