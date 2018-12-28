# PROGRAMMER: Carlos Mertens
# DATE CREATED: (DD/MM/YY) - 26/12/18
# REVISED DATE: (DD/MM/YY) - Not revise it yet
# PURPOSE: To employ several supervised algorithms to accurately model individuals' income 
#           using data collected from the 1994 U.S. Census. Choose the best candidate 
#           algorithm from preliminary results and optimize this algorithm to best model the 
#           data. Goal with this implementation is to construct a model that accurately predicts 
#           whether an individual makes more than $50,000.
#
# USAGE: This script requires Numpy, Pandas and Scikit_Learn to be installed within the Python environment. 
# 
#   Example call:
#    python train_model.py

# Imports
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def get_data(path):
    """Load csv file.
    
    Function to load csv file with the 1994 U.S. census data using Pandas and
    display it. To compute and investigate the data in order to have an idea 
    of the features and target.
    ----------
    Parameter:
        path (Str): Full path to the csv file with the dataset
    Return:
        data (dataframe): Full dataframe
    """

    # Load the data with Pandas
    data = pd.read_csv(path)
    # Call function to load data

    # Print first 5 rows of the data
    print("\n*** Load data for training ***\nView first 5 rows:")
    print(data.head())

    # Compute some percentage and print them
    n_greater_50k = len(data.groupby('income').get_group('>50K'))
    n_at_most_50k = len(data.groupby('income').get_group('<=50K'))
    greater_percent = round((float(n_greater_50k) / float(len(data)) * 100), 2)

    print("\n*** Explore data ***")
    print("Total number of datapoints: {}".format(len(data)))
    print("Individuals making more than $50,000: {}".format(n_greater_50k))
    print("Individuals making at most $50,000: {}".format(n_at_most_50k))
    print("Percentage of individuals making more than $50,000: {}%".format(greater_percent))

    return data


# Call function to load data
data = get_data('data/census.csv')


def prepare_data(data):
    """Preprocessing the data.

    Function to clean, format and restructure the data. Split the data into 
    features and target. Use logarithmic transformation to reduce skew in the
    data. Normalize the data and then apply one-hot encoding scheme.
    ----------
    Parameter:
        data (dataframe): Full dataframe
    Returns:
        features (dataframe): 
        targets (dataframe): Target labels
    """

    # Split the data into features and target labels
    income_raw = data['income']
    features_raw = data.drop('income', axis = 1)

    # Visualization in finding_donors Notebook helps identifying highly skewed features
    # Log-transform the high skewed features: capital-gain and capital-loss
    skewed = ['capital-gain', 'capital-loss']
    features_log_transformed = pd.DataFrame(data = features_raw)
    features_log_transformed[skewed] = features_raw[skewed].apply(lambda x: np.log(x + 1))

    # Normalize the features and print first 5 rows
    scaler = MinMaxScaler() # default=(0, 1)
    numerical = ['age', 'education-num', 'capital-gain', 'capital-loss', 'hours-per-week']

    features_log_minmax_transform = pd.DataFrame(data = features_log_transformed)
    features_log_minmax_transform[numerical] = scaler.fit_transform(features_log_transformed[numerical])

    print("\n*** Normalize features of the data ***\nView first 5 rows:")
    print(features_log_minmax_transform.head())

    # Perform one-hot encode scheme to features, numerical value encode to
    # targets and print first 5 rows
    features_final = pd.get_dummies(features_log_minmax_transform)
    income = income_raw.map({'<=50K': 0, '>50K':1})

    print("\n*** One-hot encode the features ***")
    print("{} total features after one-hot encoding.".format(len(features_final.columns)))
    print(features_final.head())

    return features_final, income


features_final, income = prepare_data(data)