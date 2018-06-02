# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 21:26:03 2017

@author: anish
"""

import requests
from bs4 import BeautifulSoup
import csv
import os
os.chdir("E:\\")
#f = csv.writer(open("example.csv", "w"))
with open('example1.csv','wb') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')
    page = requests.get("http://www.espn.com/college-football/rankings")
    soup = BeautifulSoup(page.content,'html.parser')
    links = soup.find_all("a")
    result = soup.findAll('table',{'class':"rankings has-team-logos"})
    head = result[0].find("thead")
    ths = head.findAll('th')
    label = [hc.get_text().encode("utf-8") for hc in ths]
    csvwriter.writerow(label)
    body = result[0].findAll('tbody')
    for row in body[0].findAll('tr'):
        tds = row.findAll('td')
        data = [bc.get_text().encode("utf-8") for bc in tds]
        print (data)
        csvwriter.writerow(data)
    csvfile.close()
