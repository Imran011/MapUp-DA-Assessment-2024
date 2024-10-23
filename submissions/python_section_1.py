#!/usr/bin/env python
# coding: utf-8

# ## Task 1: Reverse List by N Elements
# Write a function that takes a list and an integer n, and returns the list with every group of n elements reversed. If there are fewer than n elements left at the end, reverse all of them.
# 

# In[1]:


def reverse_by_n(lst, n):
    result = []
    for i in range(0, len(lst), n):
        chunk = lst[i:i + n]
        reversed_chunk = []
        for j in range(len(chunk)-1, -1, -1):
            reversed_chunk.append(chunk[j])
        result.extend(reversed_chunk)
    return result


# In[5]:


# Test cases
print(reverse_by_n([1, 2, 3, 4, 5, 6, 7, 8], 3)) 
print(reverse_by_n([1, 2, 3, 4, 5], 2))  
print(reverse_by_n([10, 20, 30, 40, 50, 60, 70], 4)) 


# ## Task 2: Lists & Dictionaries
# Write a function that takes a list of strings and groups them by their length. The result should be a dictionary where:
# - The keys are the string lengths.
# - The values are lists of strings that have the same length as the key.
# 

# In[9]:


def group_by_length(strings):
    length_dict = {}
    for string in strings:
        length = len(string)
        if length not in length_dict:
            length_dict[length] = []
        length_dict[length].append(string)
    return dict(sorted(length_dict.items()))


# In[11]:


# Test cases
print(group_by_length(["apple", "bat", "car", "elephant", "dog", "bear"])) 
# Expected: {3: ['bat', 'car', 'dog'], 4: ['bear'], 5: ['apple'], 8: ['elephant']}
print(group_by_length(["one", "two", "three", "four"]))
# Expected: {3: ['one', 'two'], 4: ['four'], 5: ['three']}


# ## Task 3: Flatten a Nested Dictionary
# You are given a nested dictionary that contains various details (including lists and sub-dictionaries). Your task is to write a Python function that flattens the dictionary such that:
# - Nested keys are concatenated into a single key with levels separated by a dot (.).
# - List elements should be referenced by their index, enclosed in square brackets (e.g., sections[0]).
# - Handle empty input gracefully.
# 
# ### Example:
# Input:
# ```python
# {
#     "road": {
#         "name": "Highway 1",
#         "length": 350,
#         "sections": [
#             {
#                 "id": 1,
#                 "condition": {
#                     "pavement": "good",
#                     "traffic": "moderate"
#                 }
#             
# {
#     "road.name": "Highway 1",
#     "road.length": 350,
#     "road.sections[0].id": 1,
#     "road.sections[0].condition.pavement": "good",
#     "road.sections[0].condition.traffic": "moderate"
# }
# }
#         ]
#     }
# }
# 

# In[14]:


def flatten_dict(nested_dict, parent_key='', sep='.'):
    items = []
    for k, v in nested_dict.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, dict):
                    items.extend(flatten_dict(item, f"{new_key}[{i}]", sep=sep).items())
                else:
                    items.append((f"{new_key}[{i}]", item))
        else:
            items.append((new_key, v))
    return dict(items)


# In[16]:


# Test case
nested_dict = {
    "road": {
        "name": "Highway 1",
        "length": 350,
        "sections": [
            {
                "id": 1,
                "condition": {
                    "pavement": "good",
                    "traffic": "moderate"
                }
            }
        ]
    }
}

print(flatten_dict(nested_dict))
# Expected Output:
# {
#     "road.name": "Highway 1",
#     "road.length": 350,
#     "road.sections[0].id": 1,
#     "road.sections[0].condition.pavement": "good",
#     "road.sections[0].condition.traffic": "moderate"
# }


# ## Task 4: Generate Unique Permutations
# You are given a list of integers that may contain duplicates. Your task is to generate all unique permutations of the list. The output should not contain any duplicate permutations.
# 
# ### Example:
# Input:
# ```pytho1, 1)
# ]
#  1, 2]
# 

# In[19]:


from itertools import permutations

def unique_permutations(nums):
    # Generate all permutations and convert to a set to remove duplicates
    return list(set(permutations(nums)))


# In[24]:


# Test case
input_list = [1, 1, 2]
print(unique_permutations(input_list))


# Question 5: Find All Dates in a Text
# Problem Statement:
# 
# You are given a string that contains dates in various formats (such as "dd-mm-yyyy", "mm/dd/yyyy", "yyyy.mm.dd", etc.). Your task is to identify and return all the valid dates present in the string.
# 
# You need to write a function find_all_dates that takes a string as input and returns a list of valid dates found in the text. The dates can be in any of the following formats:
# 
# dd-mm-yyyy
# mm/dd/yyyy
# yyyy.mm.dd
# You are required to use regular expressions to identify these dates.
# 
# Example:
# 
# Input:
# 
# text = "I was born on 23-08-1994, my friend on 08/23/1994, and another one on 1994.08.23."

# In[27]:


import re

def find_all_dates(text):
    # the regex pattern for the date formats
    pattern = r'(\d{2}-\d{2}-\d{4}|\d{2}/\d{2}/\d{4}|\d{4}\.\d{2}\.\d{2})'
    # Find all matches
    return re.findall(pattern, text)


# In[29]:


# Test case
text = "I was born on 23-08-1994, my friend on 08/23/1994, and another one on 1994.08.23."
print(find_all_dates(text))



# Question 6: Decode Polyline, Convert to DataFrame with Distances
# You are given a polyline string, which encodes a series of latitude and longitude coordinates. Polyline encoding is a method to efficiently store latitude and longitude data using fewer bytes. The Python polyline module allows you to decode this string into a list of coordinates.
# 
# Write a function that performs the following operations:
# 
# Decode the polyline string using the polyline module into a list of (latitude, longitude) coordinates.
# Convert these coordinates into a Pandas DataFrame with the following columns:
# latitude: Latitude of the coordinate.
# longitude: Longitude of the coordinate.
# distance: The distance (in meters) between the current row's coordinate and the previous row's one. The first row will have a distance of 0 since there is no previous point.
# Calculate the distance using the Haversine formula for points in successive rows.

# In[32]:



# In[1]:


import polyline
import pandas as pd
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # Haversine formula
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371000  # Radius of earth in meters
    return c * r

def decode_polyline(polyline_str):
    # Decode polyline string
    coords = polyline.decode(polyline_str)
    data = []
    previous_coord = None
    
    for i, (lat, lon) in enumerate(coords):
        if previous_coord is None:
            distance = 0
        else:
            distance = haversine(previous_coord[1], previous_coord[0], lon, lat)
        data.append({'latitude': lat, 'longitude': lon, 'distance': distance})
        previous_coord = (lat, lon)
    
    return pd.DataFrame(data)


# In[5]:


# Test case with a valid polyline
polyline_str = "_p~iF~d~uP~_@_b`@_@fJzB@dCf@fG~I^uC"
df = decode_polyline(polyline_str)
print(df)


# Question 7: Matrix Rotation and Transformation
# Write a function that performs the following operations on a square matrix (n x n):
# 
# Rotate the matrix by 90 degrees clockwise.
# After rotation, for each element in the rotated matrix, replace it with the sum of all elements in the same row and column (in the rotated matrix), excluding itself.
# The function should return the transformed matrix.
# 
# Example
# For the input matrix:
# 
# matrix = [[1, 2, 3],[4, 5, 6],[7, 8, 9]]
# Rotate the matrix by 90 degrees clockwise:
# 
# rotated_matrix = [[7, 4, 1],[8, 5, 2],[9, 6, 3]]
# Replace each element with the sum of all elements in the same row and column, excluding itself:
# 
# final_matrix = [[22, 19, 16],[23, 20, 17],[24, 21, 18]]
# 

# In[8]:


def rotate_matrix(matrix):
    n = len(matrix)
    # Rotate the matrix by 90 degrees clockwise
    rotated = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            rotated[j][n - 1 - i] = matrix[i][j]
    return rotated

def transform_matrix(matrix):
    n = len(matrix)
    transformed = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            row_sum = sum(matrix[i])  # Sum of the current row
            col_sum = sum(matrix[k][j] for k in range(n))  # Sum of the current column
            transformed[i][j] = row_sum + col_sum - matrix[i][j]  # Exclude the element itself
    return transformed

def rotate_and_transform(matrix):
    rotated = rotate_matrix(matrix)
    final_transformed = transform_matrix(rotated)
    return final_transformed


# In[10]:


matrix = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 9]]

result = rotate_and_transform(matrix)
print(result)


# Question 8: Time Check
# You are given a dataset, dataset-1.csv, containing columns id, id_2, and timestamp (startDay, startTime, endDay, endTime). The goal is to verify the completeness of the time data by checking whether the timestamps for each unique (id, id_2) pair cover a full 24-hour period (from 12:00:00 AM to 11:59:59 PM) and span all 7 days of the week (from Monday to Sunday).
# 
# Create a function that accepts dataset-1.csv as a DataFrame and returns a boolean series that indicates if each (id, id_2) pair has incorrect timestamps. The boolean series must have multi-index (id, id_2).

# In[20]:


import pandas as pd

def check_time_completeness(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Group by (id, id_2) and check for 24-hour coverage
    grouped = df.groupby(['id', 'id_2'])

    results = {}
    all_days = {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'}
    
    for (id_val, id_2_val), group in grouped:
        # Extract unique days
        unique_days = set(group['startDay'].unique())

        # Convert startTime and endTime to datetime.time format
        group['startTime'] = pd.to_datetime(group['startTime'], format='%H:%M:%S').dt.time
        group['endTime'] = pd.to_datetime(group['endTime'], format='%H:%M:%S').dt.time

        start_times = group['startTime']
        end_times = group['endTime']

        # Check if all 7 days are present
        days_covered = unique_days == all_days

        # Check if timestamps cover a full 24-hour period
        time_covered = (start_times.min() <= end_times.max())

        # Check completeness
        results[(id_val, id_2_val)] = days_covered and time_covered

    return pd.Series(results, name='Completeness')


# In[24]:


result = check_time_completeness('dataset-1.csv')
print(result)


# In[ ]:




