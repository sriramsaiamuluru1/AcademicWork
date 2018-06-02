import requests
from bs4 import BeautifulSoup
import os
import csv

os.chdir("E://")
with open('scrapped_data.csv','wb') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')

    page = requests.get('http://www.espn.com/college-football/rankings')
    soup = BeautifulSoup(page.content,'html.parser')

    result = soup.findAll('table',{'class':'rankings has-team-logos'})

    head = result[0].find('thead')

    ths = head.findAll('th')
    
    label = [hc.get_text().encode('utf-8') for hc in ths]
    print label
    csvwriter.writerow(label)

    body = result[0].findAll('tbody')
    for row in body[0].findAll('tr'):
        tds = row.findAll('td')
        data = [bc.get_text().encode('utf-8') for bc in tds]
        print data
        csvwriter.writerow(data)
    csvfile.close()