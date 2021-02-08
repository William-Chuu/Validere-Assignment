import unittest
import workspace
from sklearn.metrics import mean_squared_error
import pandas as pd
import math
# angle
# regression

class Test(unittest.TestCase):
    def test_regression1(self):
        # actual data parsed from website
        temp_actual = workspace.data(workspace.url1)

        # predicted calculated data from regression line
        x1, y1 = temp_actual['percents'], temp_actual['temp']
        m1, b1 = workspace.LOBF(x1, y1)
        temp_predicted = pd.DataFrame(temp_actual['percents'])
        temp_predicted['temp'] = temp_predicted.apply(lambda x: workspace.new_temps(x['percents'], m1, b1), axis=1)
        temp_predicted = temp_predicted['temp']

        print(temp_actual)
        print(temp_predicted)
        
        #RMSE 
        MSE = mean_squared_error(temp_actual['temp'], temp_predicted)

        RMSE = math.sqrt(MSE)
        print(RMSE)
    
    def test_regression2(self):
        # actual data parsed from website
        temp_actual = workspace.data(workspace.url2)

        # predicted calculated data from regression line
        x1, y1 = temp_actual['percents'], temp_actual['temp']
        m1, b1 = workspace.LOBF(x1, y1)
        temp_predicted = pd.DataFrame(temp_actual['percents'])
        temp_predicted['temp'] = temp_predicted.apply(lambda x: workspace.new_temps(x['percents'], m1, b1), axis=1)
        temp_predicted = temp_predicted['temp']

        print(temp_actual)
        print(temp_predicted)
        
        #RMSE 
        MSE = mean_squared_error(temp_actual['temp'], temp_predicted)

        RMSE = math.sqrt(MSE)
        print(RMSE)

if __name__ == '__main__':
    unittest.main()