#!/usr/bin/env python
# coding: utf-8

# # Python Task 1

# ### Importing necessary libraries

# In[1]:


import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
from tabulate import tabulate
import matplotlib as mat
import statistics as st
import datetime 
from dateutil import relativedelta
from datetime import datetime, timedelta
from datetime import datetime 


# ### Read the csv file as a dataframe

# In[2]:


df = pd.read_csv('dataset-1.csv')
df.head()


# # Question 1: Car Matrix Generation

# Under the function named generate_car_matrix write a logic that takes the dataset-1.csv as a DataFrame. Return a new DataFrame that follows the following rules:
# 
# * values from id_2 as columns
# * values from id_1 as index
# * dataframe should have values from car column
# * diagonal values should be 0.

# In[3]:


car_matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)

for idx in car_matrix.index:
    car_matrix.loc[idx, idx] = 0
    
car_matrix


# # Question 2: Car Type Count Calculation

# Create a Python function named get_type_count that takes the dataset-1.csv as a DataFrame. Add a new categorical column car_type based on values of the column car:
# 
# * low for values less than or equal to 15,
# * medium for values greater than 15 and less than or equal to 25,
# * high for values greater than 25.
# 
# Calculate the count of occurrences for each car_type category and return the result as a dictionary. Sort the dictionary alphabetically based on keys.

# In[4]:


def get_type_count(dataframe):
    
    dataframe['car_type'] = pd.cut(dataframe['car'], bins=[-float('inf'), 15, 25, float('inf')],
                                   labels=['low', 'medium', 'high'])

    
    type_counts = dataframe['car_type'].value_counts().to_dict()

    
    sorted_counts = dict(sorted(type_counts.items()))

    return sorted_counts

result = get_type_count(df)
print(result)


# # Question 3: Bus Count Index Retrieval

# Create a Python function named get_bus_indexes that takes the dataset-1.csv as a DataFrame. The function should identify and return the indices as a list (sorted in ascending order) where the bus values are greater than twice the mean value of the bus column in the DataFrame.

# In[5]:


def get_bus_indexes(dataframe):
    
    mean_bus = dataframe['bus'].mean()

    
    bus_indexes = dataframe[dataframe['bus'] > 2 * mean_bus].index.tolist()

    
    bus_indexes.sort()

    return bus_indexes

result = get_bus_indexes(df)
print(result)


# # Question 4: Route Filtering

# Create a python function filter_routes that takes the dataset-1.csv as a DataFrame. The function should return the sorted list of values of column route for which the average of values of truck column is greater than 7.

# In[6]:


def filter_routes(dataframe):
    
    route_avg_truck = dataframe.groupby('route')['truck'].mean()

   
    filtered_routes = route_avg_truck[route_avg_truck > 7].index.tolist()


    filtered_routes.sort()

    return filtered_routes


result = filter_routes(df)
print(result)


# # Question 5: Matrix Value Modification

# Create a Python function named multiply_matrix that takes the resulting DataFrame from Question 1, as input and modifies each value according to the following logic:
# 
# * If a value in the DataFrame is greater than 20, multiply those values by 0.75,
# * If a value is 20 or less, multiply those values by 1.25.
# 
# The function should return the modified DataFrame which has values rounded to 1 decimal place.

# In[8]:


def multiply_matrix(car_matrix):
    
    modified_matrix = car_matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

   
    modified_matrix = modified_matrix.round(1)

    return modified_matrix

modified_result = multiply_matrix(car_matrix)
modified_result


# ### Reading dataset 2 as a dataframe

# In[9]:


df = pd.read_csv('dataset-2.csv')
df.head()


# # Question 6: Time Check

# You are given a dataset, dataset-2.csv, containing columns id, id_2, and timestamp (startDay, startTime, endDay, endTime). The goal is to verify the completeness of the time data by checking whether the timestamps for each unique (id, id_2) pair cover a full 24-hour period (from 12:00:00 AM to 11:59:59 PM) and span all 7 days of the week (from Monday to Sunday).
# 
# Create a function that accepts dataset-2.csv as a DataFrame and returns a boolean series that indicates if each (id, id_2) pair has incorrect timestamps. The boolean series must have multi-index (id, id_2).

# In[10]:


def verify_time_completeness(dataframe):
    
    dataframe['start_datetime'] = pd.to_datetime(dataframe['startDay'] + ' ' + dataframe['startTime'])
    dataframe['end_datetime'] = pd.to_datetime(dataframe['endDay'] + ' ' + dataframe['endTime'])

    
    grouped = dataframe.groupby(['id', 'id_2']).agg({
        'start_datetime': 'min',
        'end_datetime': 'max'
    })

    
    completeness = (
        (grouped['start_datetime'].dt.time == pd.Timestamp('00:00:00').time()) &
        (grouped['end_datetime'].dt.time == pd.Timestamp('23:59:59').time()) &
        (grouped['start_datetime'].dt.dayofweek.min() == 0) &
        (grouped['end_datetime'].dt.dayofweek.max() == 6)
    )

    return completeness

result = verify_time_completeness(df)
result

