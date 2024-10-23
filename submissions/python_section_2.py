#!/usr/bin/env python
# coding: utf-8

# Question 9: Distance Matrix Calculation
# 
# Create a function named calculate_distance_matrix that takes the dataset-2.csv as input and generates a DataFrame representing distances between IDs.
# 
# The resulting DataFrame should have cumulative distances along known routes, with diagonal values set to 0. If distances between toll locations A to B and B to C are known, then the distance from A to C should be the sum of these distances. Ensure the matrix is symmetric, accounting for bidirectional distances between toll locations (i.e. A to B is equal to B to A).

# In[7]:


import pandas as pd

def calculate_distance_matrix(file_path):
    # Read the dataset
    df = pd.read_csv(file_path)
    
    # Create a list of unique IDs from both id_start and id_end
    unique_ids = pd.concat([df['id_start'], df['id_end']]).unique()
    
    # Initialize the distance matrix
    distance_matrix = pd.DataFrame(0, index=unique_ids, columns=unique_ids)
    
    # Fill the distance matrix with known distances
    for _, row in df.iterrows():
        start_id = row['id_start']
        end_id = row['id_end']
        distance = row['distance']
        
        # Since it's a symmetric matrix, assign distances both ways
        distance_matrix.at[start_id, end_id] = distance
        distance_matrix.at[end_id, start_id] = distance
    
    return distance_matrix

# Test the function with the dataset
distance_matrix = calculate_distance_matrix('dataset-2.csv')
print(distance_matrix)


# Question 10: Unroll Distance Matrix
# 
# Create a function unroll_distance_matrix that takes the DataFrame created in Question 9. The resulting DataFrame should have three columns: columns id_start, id_end, and distance.
# 
# All the combinations except for same id_start to id_end must be present in the rows with their distance values from the input DataFrame.

# In[10]:


import pandas as pd

def unroll_distance_matrix(distance_matrix):
    unrolled_data = []
    
    # Iterate over the distance matrix to unroll the data
    for id_start in distance_matrix.index:
        for id_end in distance_matrix.columns:
            if id_start != id_end:
                unrolled_data.append({
                    'id_start': id_start,
                    'id_end': id_end,
                    'distance': distance_matrix.at[id_start, id_end]
                })
    
    # Convert the list to a DataFrame
    unrolled_df = pd.DataFrame(unrolled_data)
    
    return unrolled_df
unrolled_df = unroll_distance_matrix(distance_matrix)
print(unrolled_df)


# Question 11: Finding IDs within Percentage Threshold
# 
# Create a function find_ids_within_ten_percentage_threshold that takes the DataFrame created in Question 10 and a reference value from the id_start column as an integer.
# 
# Calculate average distance for the reference value given as an input and return a sorted list of values from id_start column which lie within 10% (including ceiling and floor) of the reference value's average.

# In[15]:


def find_ids_within_ten_percentage_threshold(unrolled_df, reference_id):
    # Filter rows where id_start is the reference_id
    ref_data = unrolled_df[unrolled_df['id_start'] == reference_id]
    
    # Calculate the average distance for the reference_id
    avg_distance = ref_data['distance'].mean()
    
    # Define the 10% threshold range
    lower_bound = avg_distance * 0.9
    upper_bound = avg_distance * 1.1
    
    # Find ids within the threshold range
    result = unrolled_df[(unrolled_df['distance'] >= lower_bound) & 
                         (unrolled_df['distance'] <= upper_bound)]
    
    # Return the sorted list of id_start values
    return sorted(result['id_start'].unique())
reference_id = 1001400  # Example reference id
result_ids = find_ids_within_ten_percentage_threshold(unrolled_df, reference_id)
print(result_ids)


# Question 12: Calculate Toll Rate
# 
# Create a function calculate_toll_rate that takes the DataFrame created in Question 10 as input and calculates toll rates based on vehicle types.
# 
# The resulting DataFrame should add 5 columns to the input DataFrame: moto, car, rv, bus, and truck with their respective rate coefficients. The toll rates should be calculated by multiplying the distance with the given rate coefficients for each vehicle type:
# 
# 0.8 for
#  moto
# 1.2 f
# or car
# 1.5
#  for rv
# 2.2
#  for bus
# 3.6 
# for truck

# In[19]:


def calculate_toll_rate(unrolled_df):
    # Define rate coefficients for each vehicle type
    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }
    
    # Create new columns for each vehicle type by multiplying distance with the rate
    for vehicle, rate in rate_coefficients.items():
        unrolled_df[vehicle] = unrolled_df['distance'] * rate
    
    return unrolled_df
toll_rate_df = calculate_toll_rate(unrolled_df)
print(toll_rate_df.head())


# Question 13: Calculate Time-Based Toll Rates
# Create a function named calculate_time_based_toll_rates that takes the DataFrame created in Question 12 as input and calculates toll rates for different time intervals within a day.
# 
# The resulting DataFrame should have these five columns added to the input: start_day, start_time, end_day, and end_time.
# 
# start_day, end_day must be strings with day values (from Monday to Sunday in proper case)
# start_time and end_time must be of type datetime.time() with the values from time range given below.
# Modify the values of vehicle columns according to the following time ranges:
# 
# Weekdays (Monday - Friday):
# 
# From 00:00:00 to 10:00:00: Apply a discount factor of 0.8
# From 10:00:00 to 18:00:00: Apply a discount factor of 1.2
# From 18:00:00 to 23:59:59: Apply a discount factor of 0.8
# Weekends (Saturday and Sunday):
# 
# Apply a constant discount factor of 0.7 for all times.
# For each unique (id_start, id_end) pair, cover a full 24-hour period (from 12:00:00 AM to 11:59:59 PM) and span all 7 days of the week (from Monday to Sunday).

# In[ ]:


from datetime import time

def calculate_time_based_toll_rates(toll_rate_df):
    # Define time intervals and discount factors
    weekday_discounts = [
        (time(0, 0), time(10, 0), 0.8),
        (time(10, 0), time(18, 0), 1.2),
        (time(18, 0), time(23, 59, 59), 0.8)
    ]
    weekend_discount = 0.7

    # Create an empty list to store the results
    results = []
    
    # Loop through each unique pair of (id_start, id_end)
    for _, row in toll_rate_df.iterrows():
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            for start_time, end_time, factor in weekday_discounts:
                # Copy the row and adjust the toll rates
                new_row = row.copy()
                new_row['start_day'] = day
                new_row['end_day'] = day
                new_row['start_time'] = start_time
                new_row['end_time'] = end_time
                
                # Adjust the rates for all vehicle types
                for vehicle in ['moto', 'car', 'rv', 'bus', 'truck']:
                    new_row[vehicle] = row[vehicle] * factor
                
                results.append(new_row)
        
        # For weekends, apply the constant discount factor
        for day in ['Saturday', 'Sunday']:
            new_row = row.copy()
            new_row['start_day'] = day
            new_row['end_day'] = day
            new_row['start_time'] = time(0, 0)
            new_row['end_time'] = time(23, 59, 59)
            
            # Apply the weekend discount to all vehicle types
            for vehicle in ['moto', 'car', 'rv', 'bus', 'truck']:
                new_row[vehicle] = row[vehicle] * weekend_discount
            
            results.append(new_row)
    
    # Convert the results into a DataFrame
    time_based_df = pd.DataFrame(results)
    return time_based_df
time_based_toll_df = calculate_time_based_toll_rates(toll_rate_df)
print(time_based_toll_df.head())


# In[ ]:




