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
        a1, b1, c1 = workspace.regression(x1, y1)
        temp_predicted = pd.DataFrame(temp_actual['percents'])
        temp_predicted = workspace.predicted_values(a1, b1, c1, temp_predicted)['temp']
        
        #RMSE 
        MSE = mean_squared_error(temp_actual['temp'], temp_predicted)

        RMSE = math.sqrt(MSE)
        print(RMSE)
    
        self.assertTrue(RMSE < 30)
    
    def test_regression2(self):
        # actual data parsed from website
        temp_actual = workspace.data(workspace.url2)

        # predicted calculated data from regression line
        x1, y1 = temp_actual['percents'], temp_actual['temp']
        a1, b1, c1 = workspace.regression(x1, y1)
        temp_predicted = pd.DataFrame(temp_actual['percents'])
        temp_predicted = workspace.predicted_values(a1, b1, c1, temp_predicted)['temp']
        
        #RMSE 
        MSE = mean_squared_error(temp_actual['temp'], temp_predicted)

        RMSE = math.sqrt(MSE)
        print(RMSE)

        self.assertTrue(RMSE < 30)
    
    # # assuming initial curves do not intersect
    # def test_middle_mixture(self):
    #     #todo

if __name__ == '__main__':
    unittest.main()