import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver

# scraping address
addr = "http://historical.elections.virginia.gov/elections/search/year_from:1924/year_to:2016/office_id:1/stage:General"
resp = requests.get(addr)
html = resp.content
soup = bs(html, "html.parser")

# create empty lists for election data
electionID = []
temp = []

# series of for loops to populate lists with relevant entries
for rows in soup.find_all(['tr', 'td']):
    ID = rows.get('id')
    year = rows.find('td', {"class": "year first"})
    id_year = [year, ID]
    temp.append(id_year)

for k in range(0, len(temp)):
    if temp[k][0] != None:
        electionID.append(temp[k])

for l in range(0, len(electionID)):
    electionID_year = electionID[l][0]
    year = electionID_year.text
    electionID_id = electionID[l][1].replace("election-id-", "")
    to_push = [year, electionID_id]
    electionID[l] = to_push
