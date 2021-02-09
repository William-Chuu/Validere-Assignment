import unittest
import workspace
from sklearn.metrics import mean_squared_error
import pandas as pd
import math

class Test(unittest.TestCase):
    # gathers neccessary info and calculates the Root Mean Square Error (RMSE)
    # root mean square error test should be less than 30 (RMSE of linear regression model)
    # Oil 1
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
        print('url1 RSME: {}'.format(RMSE))
    
        self.assertTrue(RMSE < 30)
    
    # Oil 2
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
        print('url2 RSME: {}'.format(RMSE))

        self.assertTrue(RMSE < 30)
    
    # assuming initial curves do not intersect, equal volumes and oil 2 is curve with larger values
    # mixture temp should be in between oil 1 and oil2 point
    def test_middle_mixture(self):
        # mixture dataframe
        mixture_df = workspace.main(workspace.url1, 1, workspace.url2, 1)
        oil1 = workspace.data(workspace.url1)
        oil2 = workspace.data(workspace.url2)

        x1, y1 = oil1['percents'], oil1['temp']
        x2, y2 = oil2['percents'], oil2['temp']

        a1, b1, c1 = workspace.regression(x1, y1)
        a2, b2, c2 = workspace.regression(x2, y2)

        # oil dataframes
        oil1_df = pd.DataFrame({'percents': [5,10,20,30,40,50,60,70,80,90,95,99]})
        oil1_df = workspace.predicted_values(a1, b1, c1, oil1_df)
        oil2_df = pd.DataFrame({'percents': [5,10,20,30,40,50,60,70,80,90,95,99]})
        oil2_df = workspace.predicted_values(a2, b2, c2, oil2_df)

        # using arbitrary middle point (50%)
        print('mixture estimated 50% point: {}'.format(mixture_df.iloc[5,1]))
        print('oil2 estimated 50% point: {}'.format(oil2_df.iloc[5,1]))
        print('oil1 estimated 50% point: {}'.format(oil1_df.iloc[5,1]))

        # mixture point is less than oil2
        self.assertTrue(mixture_df.iloc[5,1] < oil2_df.iloc[5,1])
        # mixture point is greater than oil1
        self.assertTrue(mixture_df.iloc[5,1] > oil1_df.iloc[5,1])
    
    # assuming you can use the volumes as a multiplication factor 
    # mixture curve should gravitate towards larger volume oil

    #larger oil 2 volume factor
    def test_volume_factor1(self):
        # good old pythagorean theorem
        def point_distance(x1, y1, x2, y2):
            dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            return dist
        # mixture dataframe
        mixture_df = workspace.main(workspace.url1, 1, workspace.url2, 10)
        oil1 = workspace.data(workspace.url1)
        oil2 = workspace.data(workspace.url2)

        x1, y1 = oil1['percents'], oil1['temp']
        x2, y2 = oil2['percents'], oil2['temp']

        a1, b1, c1 = workspace.regression(x1, y1)
        a2, b2, c2 = workspace.regression(x2, y2)

        # oil dataframes
        oil1_df = pd.DataFrame({'percents': [5,10,20,30,40,50,60,70,80,90,95,99]})
        oil1_df = workspace.predicted_values(a1, b1, c1, oil1_df)
        oil2_df = pd.DataFrame({'percents': [5,10,20,30,40,50,60,70,80,90,95,99]})
        oil2_df = workspace.predicted_values(a2, b2, c2, oil2_df)

        # calc distances
        oil2_to_mixture = point_distance(50, mixture_df.iloc[5,1], 50, oil2_df.iloc[5,1])
        oil1_to_mixture = point_distance(50, mixture_df.iloc[5,1], 50, oil1_df.iloc[5,1])

        self.assertTrue(oil2_to_mixture < oil1_to_mixture)

    #larger oil 1 volume factor
    def test_volume_factor2(self):
        # good old pythagorean theorem
        def point_distance(x1, y1, x2, y2):
            dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            return dist
        # mixture dataframe
        mixture_df = workspace.main(workspace.url1, 5, workspace.url2, 1)
        oil1 = workspace.data(workspace.url1)
        oil2 = workspace.data(workspace.url2)

        x1, y1 = oil1['percents'], oil1['temp']
        x2, y2 = oil2['percents'], oil2['temp']

        a1, b1, c1 = workspace.regression(x1, y1)
        a2, b2, c2 = workspace.regression(x2, y2)

        # oil dataframes
        oil1_df = pd.DataFrame({'percents': [5,10,20,30,40,50,60,70,80,90,95,99]})
        oil1_df = workspace.predicted_values(a1, b1, c1, oil1_df)
        oil2_df = pd.DataFrame({'percents': [5,10,20,30,40,50,60,70,80,90,95,99]})
        oil2_df = workspace.predicted_values(a2, b2, c2, oil2_df)

        # calc distances
        oil2_to_mixture = point_distance(50, mixture_df.iloc[5,1], 50, oil2_df.iloc[5,1])
        oil1_to_mixture = point_distance(50, mixture_df.iloc[5,1], 50, oil1_df.iloc[5,1])

        self.assertTrue(oil2_to_mixture > oil1_to_mixture)


if __name__ == '__main__':
    unittest.main()