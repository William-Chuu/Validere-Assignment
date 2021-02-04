import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.crudemonitor.ca/crudes/dist.php?acr=MSW&time=recent"
# scrapes the URL for percentages and temps
# returns as panda
def data(url):
    # http request on URL, retrieves HTML data as Python Object
    page = requests.get(url)
    # use appropriate parser to get html content
    soup = BeautifulSoup(page.content, 'html.parser')

    # extract table with percentages and temp
    body = soup.find('tbody', attrs={'class': None})
    # tr are rows of table
    rows = body.findAll('tr')

    # all percentages use 'th' tag (skip first one since it is IPB and not a percentage)
    # loop over each percent and convert to text (get rid of tags)
    percents = [p.getText() for p in (body.findAll('th')[1:])]

    # loop over each row
    # note Find and not findAll which looks for first 'td' tag with class=celcius (there are avg, std dev)
    temp_rows = [row.find('td', class_='celsius') for row in rows[1:]]
    # convert to text
    temp = [temp.getText() for temp in temp_rows]

    # temp in one line but easier for me to understand above
    # temp = [[td.getText() for td in row.find('td', class_='celsius')]
    #             for row in rows[1:11]]
    
    # print (temp)
    # print (percents)
    d = {'percents': percents, 'temp': temp}

    return(pd.DataFrame(d))
    # print(stats)
    
data(url)