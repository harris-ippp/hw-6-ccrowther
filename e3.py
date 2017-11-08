import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver

addr = "http://historical.elections.virginia.gov/elections/search/year_from:1924/year_to:2016/office_id:1/stage:General"
resp = requests.get(addr)
html = resp.content
soup = bs(html, "html.parser")

electionID = []
temp = []

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

for m in range(0, len(electionID)):
    year = electionID[m][0]
    file = year +'.csv'
    ID = str(electionID[m][1])
    link = 'http://historical.elections.virginia.gov/elections/download/%s/precincts_include:0/'%ID
    resp = requests.get(link)
    with open(file, "w") as my_csv:
        my_csv.write(resp.text)

# new code for 3:
import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver

dataframes = [] # create empty list for dataframe

for n in range(0,len(electionID)): # for loop to go through .csv files
    filename = electionID[n][0]+".csv"

    party_candidate = pd.read_csv(filename, nrows = 1).dropna(axis=1) # first row of the file
    party_candidate_dict = party_candidate.iloc[0].to_dict() # turn it into a dictionary

    votes_df = pd.read_csv(filename, index_col = 0, thousands = ',', skiprows = [1]) # open dataframe

    votes_df.rename(inplace = True, columns = party_candidate_dict) # rename first row of dataframe with dictionary names
    votes_df.dropna(inplace = True, axis = 1) # drop columns without entries
    votes_df["Year"] = electionID[n][0]

    votes_df = votes_df[["Year","Democratic","Republican", "Total Votes Cast"]] # select the listed columns from the dataframe
    votes = votes_df.head()

    dataframes.append(votes) # append votes to the dataframe

results = pd.concat(dataframes) # put the dataframes together

results["Republican Share"] = results["Republican"]/results["Total Votes Cast"] # calculate vote share for Reps
results["Democrat Share"] = results["Democratic"]/results["Total Votes Cast"] # and for Dems

# Accomack County Plot
accomack_county_df = results[results.index == "Accomack County"]
accomack_bar = accomack_county_df.plot.bar(x = "Year", y=["Republican Share", "Democrat Share"])
accomack_bar.set_ylabel("Percent of Votes")
accomack_bar.set_ylim([0,1])
accomack_bar.set_yticklabels(['{:3.2f}%'.format(x*100) for x in accomack_bar.get_yticks()] )
plt.title("Accomack County Share of Votes")
accomack_bar.figure.savefig("Accomack County.pdf")
plt.show()

# Alexandria County Plot
Alexandria_df = results[results.index == "Alexandria City"]
Alexandria_bar = Alexandria_df.plot.bar(x = "Year", y=["Republican Share", "Democrat Share"])
Alexandria_bar.set_ylabel("Percent of Votes")
Alexandria_bar.set_ylim([0,1])
Alexandria_bar.set_yticklabels(['{:3.2f}%'.format(x*100) for x in Alexandria_bar.get_yticks()])
plt.title("Alexandria City Share of Votes")
Alexandria_bar.figure.savefig("Alexandria City.pdf")
plt.show()

# Alleghany County Plot
Alleghany = results[results.index == "Alleghany County"]
Alleghany_bar = Alleghany.plot.bar(x = "Year", y=["Republican Share", "Democrat Share"])
Alleghany_bar.set_ylabel("Percent of Votes")
Alleghany_bar.set_ylim([0,1])
Alleghany_bar.set_yticklabels(['{:3.2f}%'.format(x*100) for x in Alleghany_bar.get_yticks()] )
plt.title("Alleghany County Share of Votes")
Alleghany_bar.figure.savefig("Alleghany County.pdf")
plt.show()

#Amelia County Plot
Amelia = results[results.index == "Amelia County"]
Amelia_bar = Amelia.plot.bar(x = "Year", y=["Republican Share", "Democrat Share"])
Amelia_bar.set_ylabel("Percent of Votes")
Amelia_bar.set_ylim([0,1])
Amelia_bar.set_yticklabels(['{:3.2f}%'.format(x*100) for x in Amelia_bar.get_yticks()] )
plt.title("Amelia County Share of Votes")
Amelia_bar.figure.savefig("Amelia County.pdf")
plt.show()
