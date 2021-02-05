import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from matplotlib import pyplot
from scipy.optimize import curve_fit
from numpy import arange

url1 = "https://www.crudemonitor.ca/crudes/dist.php?acr=MSW&time=recent"
url2 = "https://www.crudemonitor.ca/crudes/dist.php?acr=BCL&time=recent"

# objective function to fit a line to data
def objective(m, x, b):
    return(m * x + b)

def main(url1, vol1, url2, vol2):
    tot_vol = vol1 + vol2
    oil1_factor = vol1 / tot_vol
    oil2_factor = vol2 / tot_vol

    oil1, oil2 = data(url1), data(url2)

    # choose the input and output variables
    x1, y1 = oil1['percents'], oil1['temp']
    x2, y2 = oil2['percents'], oil2['temp']
    m1, b1 = LOBF(x1, y1)
    m2, b2 = LOBF(x2, y2)
    print(m1,b1,m2,b2)

    mixture_m = (oil1_factor * m1) + (oil2_factor * m2)
    mixture_b = (oil1_factor * b1) + (oil2_factor * b2)

    mixture_df = pd.DataFrame({'percents': [5,10,20,30,40,50,60,70,80,90,95,99], 'temp': [0,0,0,0,0,0,0,0,0,0,0,0]})
    mixture_df['temp'] = mixture_df.apply(lambda x: new_temps(x['percents'], mixture_m, mixture_b), axis=1)
    print(mixture_df)



    

    # # plot input vs output
    # pyplot.scatter(x, y)
    # # define a sequence of inputs between the smallest and largest known inputs
    # x_line = arange(min(x), max(x), 1)
    # # calculate the output for the range
    # y_line = objective(x_line, m, b)
    # # create a line plot for the mapping function
    # pyplot.plot(x_line, y_line, '--', color='red')
    # pyplot.show()

# calculates new temp of mixture
def new_temps(percent, m, b):
    return((m * percent) + b)

# takes x and y data as params
# returns string of curve fit slope and y-int
def LOBF(x, y):
    # curve fit
    # popt is type N-dimensional array (ndarray) with the optimal m and b values
    popt, _ = curve_fit(objective, x, y)
    # summarize the parameter values
    m, b = popt
    return (m, b)

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

# data(url1)
main(url1, 1, url2, 1)

