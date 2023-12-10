#!/usr/bin/env python
# coding: utf-8

# # Python Task 2

# ### Importing necessary libraries

# In[1]:


import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
from tabulate import tabulate
import matplotlib as mat
import statistics as st


# ### Read the data set as dataframe

# In[2]:


df = pd.read_csv('dataset-3.csv')
df.head()


# # Question 1: Distance Matrix Calculation

# Create a function named calculate_distance_matrix that takes the dataset-3.csv as input and generates a DataFrame representing distances between IDs.
# 
# The resulting DataFrame should have cumulative distances along known routes, with diagonal values set to 0. If distances between toll locations A to B and B to C are known, then the distance from A to C should be the sum of these distances. Ensure the matrix is symmetric, accounting for bidirectional distances between toll locations (i.e. A to B is equal to B to A).

# In[3]:


import pandas as pd

def calculate_distance_matrix(file_path):
    
    data = pd.read_csv(file_path)
    
    unique_ids = sorted(set(data['id_start']).union(set(data['id_end'])))
    distance_matrix = pd.DataFrame(0, index=unique_ids, columns=unique_ids)
    
    for idx, row in data.iterrows():
        start = row['id_start']
        end = row['id_end']
        distance = row['distance']
        
       
        distance_matrix.at[start, end] = distance
        distance_matrix.at[end, start] = distance 
        
    for i in unique_ids:
        for j in unique_ids:
            if i != j:
                for k in unique_ids:
                    if i != k and j != k:
                        if distance_matrix.at[i, k] == 0 and distance_matrix.at[i, j] != 0 and distance_matrix.at[j, k] != 0:
                            distance_matrix.at[i, k] = distance_matrix.at[i, j] + distance_matrix.at[j, k]
                            distance_matrix.at[k, i] = distance_matrix.at[i, k]
    
  
    distance_matrix.values[[range(len(unique_ids))]*2] = 0
    
    return distance_matrix


# In[4]:


resulting_matrix = calculate_distance_matrix('dataset-3.csv')
resulting_matrix


# # Question 2: Unroll Distance Matrix

# Create a function unroll_distance_matrix that takes the DataFrame created in Question 1. The resulting DataFrame should have three columns: columns id_start, id_end, and distance.
# 
# All the combinations except for same id_start to id_end must be present in the rows with their distance values from the input DataFrame.

# In[5]:


import itertools


def unroll_distance_matrix(distance_matrix):
    indices = distance_matrix.index
    columns = distance_matrix.columns
    
   
    combinations = list(itertools.product(indices, columns))
    
 
    id_starts = []
    id_ends = []
    distances = []
    
  
    for start, end in combinations:
        if start != end:
            distance = distance_matrix.at[start, end]
            id_starts.append(start)
            id_ends.append(end)
            distances.append(distance)
    

    unrolled_distances = pd.DataFrame({
        'id_start': id_starts,
        'id_end': id_ends,
        'distance': distances
    })
    
    return unrolled_distances


# In[6]:


unrolled_data = unroll_distance_matrix(resulting_matrix)
unrolled_data


# # Question 3: Finding IDs within Percentage Threshold

# Create a function find_ids_within_ten_percentage_threshold that takes the DataFrame created in Question 2 and a reference value from the id_start column as an integer.
# 
# Calculate average distance for the reference value given as an input and return a sorted list of values from id_start column which lie within 10% (including ceiling and floor) of the reference value's average.

# In[7]:


def find_ids_within_ten_percentage_threshold(data_frame, reference_value):
   
    avg_distance = data_frame[data_frame['id_start'] == reference_value]['distance'].mean()
    
   
    threshold = avg_distance * 0.1
    
   
    ids_within_threshold = data_frame[(data_frame['distance'] >= avg_distance - threshold) & (data_frame['distance'] <= avg_distance + threshold)]['id_start']
    
   
    return sorted(ids_within_threshold.unique())


# In[8]:


reference_value = 1001400  
ids_within_threshold = find_ids_within_ten_percentage_threshold(unrolled_data, reference_value)
print(ids_within_threshold)


# In[9]:


data_frame = pd.DataFrame({'ID':ids_within_threshold })
print(data_frame)


# # Question 4: Calculate Toll Rate

# Create a function calculate_toll_rate that takes the DataFrame created in Question 2 as input and calculates toll rates based on vehicle types.
# 
# The resulting DataFrame should add 5 columns to the input DataFrame: moto, car, rv, bus, and truck with their respective rate coefficients. The toll rates should be calculated by multiplying the distance with the given rate coefficients for each vehicle type:
# 
# * 0.8 for moto
# * 1.2 for car
# * 1.5 for rv
# * 2.2 for bus
# * 3.6 for truck

# In[10]:


def calculate_toll_rate(data_frame):
    
    data_frame['moto'] = data_frame['distance'] * 0.8
    data_frame['car'] = data_frame['distance'] * 1.2
    data_frame['rv'] = data_frame['distance'] * 1.5
    data_frame['bus'] = data_frame['distance'] * 2.2
    data_frame['truck'] = data_frame['distance'] * 3.6
    
    return data_frame

data_with_toll_rates = calculate_toll_rate(unrolled_data)
data_with_toll_rates


# # Question 5: Calculate Time-Based Toll Rates

# Create a function named calculate_time_based_toll_rates that takes the DataFrame created in Question 3 as input and calculates toll rates for different time intervals within a day.
# 
# The resulting DataFrame should have these five columns added to the input: start_day, start_time, end_day, and end_time.
# 
# * start_day, end_day must be strings with day values (from Monday to Sunday in proper case)
# * start_time and end_time must be of type datetime.time() with the values from time range given below.
# 
# Modify the values of vehicle columns according to the following time ranges:
# 
# Weekdays (Monday - Friday):
# 
# * From 00:00:00 to 10:00:00: Apply a discount factor of 0.8
# * From 10:00:00 to 18:00:00: Apply a discount factor of 1.2
# * From 18:00:00 to 23:59:59: Apply a discount factor of 0.8
# 
# Weekends (Saturday and Sunday):
# 
# * Apply a constant discount factor of 0.7 for all times.
# 
# For each unique (id_start, id_end) pair, cover a full 24-hour period (from 12:00:00 AM to 11:59:59 PM) and span all 7 days of the week (from Monday to Sunday).

# In[11]:


import pandas as pd
from datetime import time

def calculate_time_based_toll_rates(data_frame):
    
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    time_ranges = [
        (time(0, 0, 0), time(10, 0, 0), 0.8),
        (time(10, 0, 0), time(18, 0, 0), 1.2),
        (time(18, 0, 0), time(23, 59, 59), 0.8)
    ]
    
    
    result_rows = []
    
   
    for start_time, end_time, factor in time_ranges:
        for start_day in days_of_week:
            for end_day in days_of_week:
                result_rows.append({
                    'start_day': start_day,
                    'start_time': start_time,
                    'end_day': end_day,
                    'end_time': end_time,
                })
    
    
    result_df = pd.DataFrame(columns=['start_day', 'start_time', 'end_day', 'end_time'])
    
   
    if result_rows:
        result_df = pd.DataFrame(result_rows)
    
   
    weekday_factors = {range(0, 10000): 0.8, range(10000, 180000): 1.2, range(180000, 240000): 0.8}
    weekend_factor = 0.7
    
    for idx, row in result_df.iterrows():
        start_time = row['start_time']
        end_time = row['end_time']
        start_day = row['start_day']
        end_day = row['end_day']
        
       
        if start_day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            factor = weekday_factors[(start_time.hour * 10000) + (start_time.minute * 100) + start_time.second]
        else:
            factor = weekend_factor
        
        
        data_frame.loc[(data_frame['id_start'] == data_frame['id_end']) & (data_frame['start_day'] == start_day) & (data_frame['end_day'] == end_day), f'{start_time.strftime("%H:%M:%S")}_{end_time.strftime("%H:%M:%S")}'] = data_frame['distance'] * factor
    
    return data_frame


# In[12]:


data_with_time_based_toll_rates = calculate_time_based_toll_rates(data_frame)
print(data_with_time_based_toll_rates)

