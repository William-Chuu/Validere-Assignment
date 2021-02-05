import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from matplotlib import pyplot

url = "https://www.crudemonitor.ca/crudes/dist.php?acr=MSW&time=recent"

def main(url1, vol1, url2, vol2):
    x = data(url)
    x.plot.scatter('percents', 'temp')
    pyplot.show()


# objective function to fit a line to data
def objective(y, m, x, b):
    return(m * x + b)



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

    # create dict to be able to make into pandas
    d = {'percents': percents, 'temp': temp}
    df = pd.DataFrame(d)
    # remove rows with '-'
    df = df[df.temp != '-']
    # convert all data types to floats
    df = df.astype(float)
    # print(df['temp'].dtypes)
    return(df)
    
main(url, 0, 0, 0)

