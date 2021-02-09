import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from matplotlib import pyplot
from scipy.optimize import curve_fit
from numpy import arange

url1 = "https://www.crudemonitor.ca/crudes/dist.php?acr=MSW&time=recent"
url2 = "https://www.crudemonitor.ca/crudes/dist.php?acr=AHS&time=recent"

# objective function to fit a line to data
def objective(x, a, b, c):
	return (a * x + b * x**2 + c)

def main(url1, vol1, url2, vol2):
    # multiplication factor from volumes
    tot_vol = vol1 + vol2
    oil1_factor = vol1 / tot_vol
    oil2_factor = vol2 / tot_vol

    # call data function to retrieve distillation profiles in pandas
    oil1, oil2 = data(url1), data(url2)

    # choose the independent and dependent variables
    x1, y1 = oil1['percents'], oil1['temp']
    x2, y2 = oil2['percents'], oil2['temp']

    # using curve fit function, retrieve regression curve coefficients
    a1, b1, c1 = regression(x1, y1)
    a2, b2, c2 = regression(x2, y2)

    # calculate mixture variables
    mixture_a = (oil1_factor * a1) + (oil2_factor * a2)
    mixture_b = (oil1_factor * b1) + (oil2_factor * b2)
    mixture_c = (oil1_factor * c1) + (oil2_factor * c2)

    # estimate mixture data in pandas
    mixture_df = pd.DataFrame({'percents': [5,10,20,30,40,50,60,70,80,90,95,99]})
    mixture_df = predicted_values(mixture_a, mixture_b, mixture_c, mixture_df)

    mixture_x, mixture_y = mixture_df['percents'], mixture_df['temp']

    #plot
    oilplot(x1, y1, a1, b1, c1, 'Oil 1: {}'.format(equation_label(a1, b1, c1)), 'blue')
    oilplot(x2, y2, a2, b2, c2, 'Oil 2: {}'.format(equation_label(a2, b2, c2)), 'orange')
    oilplot(mixture_x, mixture_y, mixture_a, mixture_b, mixture_c, 'Mixture: {}'.format(equation_label(mixture_a, mixture_b, mixture_c)), 'green')
    
    pyplot.legend()
    pyplot.xlabel('Percents [%]')
    pyplot.ylabel('Temps [Degrees Celsius]')
    pyplot.title('Crude Oil Mixture Distillation Curve')    
    
    pyplot.show()

    # return mixture data as pandas
    return(mixture_df)

#####
# HELPER FUNCTIONS
#####

# for legend of graph
def equation_label(a, b, c):
    return ('{:.2f} * x + {:.2f} * x**2 + {:.2f}'.format(a, b, c))

# Given coefficients, axis label and line colour
# plots 
def oilplot(x, y, a, b, c, lab, col):
    # plot input vs output
    pyplot.scatter(x, y, label=lab)
    # define a sequence of inputs between the smallest and largest known inputs
    x_line = arange(min(x), max(x), 1)
    # calculate the output for the range
    y_line = objective(x_line, a, b, c)
    # create a line plot for the mapping function
    pyplot.plot(x_line, y_line, '--', color=col)

# takes newly calculated regression coefficients and df with appropriate percents as parameters)
# returns pandas with predicted temps
def predicted_values(a, b, c, new_df):
    # calculates new temp of mixture using regression line equation
    def new_temps(percent, a, b, c):
        return(a * percent + b * percent**2 + c)

    new_df['temp'] = new_df.apply(lambda x: new_temps(x['percents'], a, b, c), axis=1)
    return new_df

# calculates new temp of mixture using regression line equation
def new_temps(percent, a, b, c):
    return(a * percent + b * percent**2 + c)

# takes x and y data as params
# returns string of curve fit slope and y-int
def regression(x, y):
    # curve fit
    # popt is type N-dimensional array (ndarray) with the optimal m and b values
    popt, _ = curve_fit(objective, x, y)
    # summarize the parameter values
    a, b, c = popt
    return (a,b,c)

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

    # create dict to be able to make into pandas
    d = {'percents': percents, 'temp': temp}
    df = pd.DataFrame(d)

    # remove rows with '-'
    df = df[df.temp != '-']
    # convert all data types to floats
    df = df.astype(float)
    # print(df['temp'].dtypes)

    return(df)


# main(url1, 1, url2, 1)

