# About The Project
Given any two crude oils with their given distillation profiles, create a model which will give an
approximate distillation profile of the mixture of the two oils with specified volumes. 

Distillation profile data can be found at: https://www.crudemonitor.ca/

My model takes the URL of the crude oils and their respective volumes as arguments. The Beautiful Soup library allows for the automated extraction of the oils Distillation Profile data where it is then run through polynomial regressions to achieve a curve fit function. These functions are then summed to obtain an approximation of the mixtures Distillation Profile.

Tests are run in order to validate the model. A series of tests confirm the accuracy of the curve fit using the Root Mean Square Error (RMSE) method is used as well as tests to cover proper results for the volume factor and predicted mixture curve.

# Getting Started
Activate virtual env:
```
env\Scripts\activate
```
To run workspace:
```
python workspace.py
```
To run tests:
```
python test.py
```

# Initial Thoughts:
Looking over the entire problem, I had no leads on how I would be able to combine 2 independent models into one mixture model without going into the chemical properties and reactions that would occur during this process. Using the fact that it is recommended in the problem to “think of the distillation profiles as snapshots of functions”, I knew that this was a key piece of information that I needed to leverage and from here, I had a general idea of how to approach this problem. 

# Assumptions
- You are able to add distillation profiles to achieve a profile of their mixture
- The volumes of each oil is a valid representation of how “strong” each individual oils distillation properties are within the mixture (can be seen as a multiplication factor)
- For simplicity for testing, assume that one oil has larger temperature values than the other oil and the 2 curves do not intersect (for example, the 2 oils below)
  - https://www.crudemonitor.ca/crudes/dist.php?acr=MSW&time=recent
  - https://www.crudemonitor.ca/crudes/dist.php?acr=AHS&time=recent

# Process
## Data Extraction
To automate the data extraction process, I took advantage of web scrapping using the Beautiful Soup library. I was able to write a function that took the URL of the oil as a parameter, parse through the HTML content and extract only the temperatures and percents from the distillation profile. This data would then be filtered, stored and returned in a pandas dataframe.

One of the issues I ran into during this process was that some of the oils would have no data for certain percentages so for example, the 99% row would contain a hyphen. Since these hyphens cannot be processed in my model, I needed to filter the data to obtain usable data. I couldn’t just replace these hyphens with 0s since this would drastically affect the curve fit and so I had to delete the rows. The last step was to convert all the data to numerical data types so that I can process it. 

## Curve Fitting
This process must be done to get an approximate function that can be used to represent the distillation profiles of each individual oil and also predict the mixture profile as wellI. 

I was not familiar with curve fitting methods prior to this project and so I did some research on common methods. I came across methods such as linear regression, piece-wise curve fitting and also a much more complicated kernel method of curve fitting. I decided to take the route of regression for a few reasons:
- Seemed the simplest and most applicable to my needs
- From observation, the distillation profiles were quite close to linear so it would be easy to perform
- Versatile. Meaning I can adjust the type of regression which will give me curves that can fit my data more accurately 

I used the curve_fit function from the SciPy library which took an objective function as a parameter (basically the degree of your regression) and the x and y data points I extracted. From here, I received a ndarray that contained the optimal coefficients for my function.

## Putting it All Together
In my main function:

- Calculate the fraction of each oils volume in the mixture (this would be the multiplication factor)
- Call my data extraction function to receive the distillation profile data for both oils
- Perform a polynomial regression to obtain the optimal coefficients of a curve fit for each oil
- Using the multiplication factors of each oil coupled with the curve fits coefficients, I can now obtain the mixture functions coefficients (and also the approximated function for the mixture). This is only valid because of the assumptions that the volumes work like multiplication factors and that I am able to add the distillation profiles like functions
- Using the function for the mixture, I create a pandas dataframe for the mixture. This process works by initially inputting the necessary percent values from 5-99% and then applying a helper function to each row that calculates the predicted temperature value given the corresponding percent value (similar to looping through every row and using the percent value as the independent variable in my mixture function)
- Using MatPlotLib, I can now plot the 2 initial oil data points, their corresponding curve fit and the mixture profile on one plot to show
- This function ends by returning the approximated data points for the mixture in a pandas dataframe

## Testing
I interpreted the instructions of “write tests” meaning that I should verify that my model is in fact, correct. I looked into typical data science testing methods such as the train/test method as well as the cross validation method, but without the presence of labeled data that represents what is supposed to be the results of mixing 2 oils, these methods were not feasible and I couldn’t refine and test my model. 

### Root Mean Square Error (RMSE)
What I could test within my model was the accuracy of my regressions to see if I was even getting a good enough representation of the oil distillation profiles in the first place. Using the unittest module in python, I wrote a RMSE test for each oil regression. Both these tests worked the same way by gathering the actual data and the predicted data from my regression to calculate the RMSE via the mean_squared_error function in the SciKit-Learn library.

Initially, I was getting RMSE values around 30 for each oil using a linear regression. I was not sure if this was an acceptable error value but judging from the temperature range of 0 - 700 degrees celsius, I would say that this value is not terrible but not good either. I would use this value as a baseline for my test to make sure that a linear regression is the least accurate my curve fit would be. I adjusted my objective function and code to represent a polynomial regression to the second degree and this time, I was getting RMSE values around 18 which was an improvement. I could continue to increase the polynomial degree until I reach a minimum RMSE value to achieve an optimal reduction in error, but this would take a decent amount of time and I was aiming for completion. 

### Volume Factor
To test if the volume multiplication factor assumption was indeed being put to use correctly, I wrote a test for each oil. In theory, the final mixture curve should gravitate towards the oil curve with the larger volume due to the multiplication factor assumption. Note, to make this test work, I also had to apply the assumption that the 2 oil curves did not intersect and that one had larger temperature values than the other. 

To test this, I wrote a unit test that calculate the distance between an arbitrary percentage on the mixture curve (chose 50%) and the same point on one of the oil curves. I did this for both oil curves and therefore had 2 distances - a distance from the mixture point to oil point 1 and from the mixture point to oil point 2. This test checked if oil with the larger volume had a smaller distance to the mixture curve point and so this would confirm if the difference in volumes affected how “strong” their distillation characteristics  were in the mixture.

### Mixture Curve in Between
Again, under the assumptions that the 2 oil curves do not intersect and that one has larger values than the other, in theory, the mixture curve should be in between the 2 oil curves. 

To test this, I picked an arbitrary percentage value, and obtained the oil1, oil2 and mixture temperatures at that x-value. After checking which of the 2 oil values are larger, I would test to see if the mixture temperature is between the 2 oil values. 

# Potential Issues/Improvements
- Non-uniform data
  - Creating curves with 10 points and 9 points depending on data creates a little bit of variance
- Web scraping dependent on the html not changing
  - Parse data and implement into a database to avoid this as well as faster read times
- Cleaner code design
  - A lot of redundancy in testing (led to long test times)
