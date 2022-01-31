# Define the necessary imports
import glob
import json
import os

import pandas as pd
import numpy as np

# List multiple JSON files in a folder
json_dir = 'data'

json_pattern = os.path.join(json_dir, '*.json')
file_list = glob.glob(json_pattern)

# Read and merge multiple JSON file into DataFrame
dfs = []
for file in file_list:
    with open(file) as f:
        json_data = pd.json_normalize(json.loads(f.read()))
        json_data['site'] = file.rsplit("/", 1)[-1]
    dfs.append(json_data)
df = pd.concat(dfs)

# Set the index to the user_id
df.set_index("user_id", inplace=True)

# Filter out non-run activities
all_runs_df = df.loc[df['type'] == 'run']
# print(all_runs_df)

# Accept as input a single user id
user_id = input("Enter user id: ")

# Create a DataFrame filtered using the inputted user_id
user_df = all_runs_df.loc[user_id]

# Create a copy of the user_df
format_datetime_df = user_df.copy()

# Convert the start and end to a datetime format
format_datetime_df[['start', 'end']] = format_datetime_df[['start', 'end']].apply(pd.to_datetime, errors='coerce')

# Sort by the start date/time in ascending
format_datetime_df = format_datetime_df.sort_values(by='start', ascending=True)

# Create a helper index that allows iteration by week while also considering the year
format_datetime_df['grp_idx'] = format_datetime_df['start'].apply(lambda x: '%s-%s' % (x.year, '{:02d}'.format(x.week)))


# Function to return the total distance for each week
def total_distance_for_week(formatted_df):
    sum_distance_for_week = formatted_df['distance'].sum()
    return sum_distance_for_week


# Create a NumPy array to store the total distance for each week
distance_for_week = np.array([])
# Append the total distance for each week to the array
distance_for_week = np.append(distance_for_week, format_datetime_df.groupby('grp_idx').apply(total_distance_for_week))
# Count the number of times the total distance for each week was > 10km
number_of_weeks_over_10km = np.count_nonzero(distance_for_week > 10)

# Create a copy of the format_datetime_df
# This DataFrame will be used to see if the user ran > 1km in a single run 3 days in a row
repeat_runner_df = format_datetime_df.copy()

# Filter out runs <= 1km
repeat_runner_df = repeat_runner_df.loc[repeat_runner_df['distance'] > 1]

# Get the date portion from 'start'
repeat_runner_df['date'] = repeat_runner_df['start'].dt.date
# Drop days with more than 1 run from the DataFrame
repeat_runner_df = repeat_runner_df.drop_duplicates(subset=['date'], keep='first')

# Put the dates into groups based on whether or not there are consecutive days
repeat_runner_df['grp_date'] = repeat_runner_df.date.diff().dt.days.fillna(1).ne(1).cumsum()
# Count the number of occurrences of a group
count = repeat_runner_df.groupby('grp_date').grp_date.count()
# Determine the number of times the user has ran > 1km in a single run three days in a row
number_of_times_over_1km_three_days_in_row = len(count.where((count > 2) & (count < 4)).dropna())

# Create a copy of the format_datetime_df
# This DataFrame will be used to see if the user ran at more of an incline or more of a decline
elevation = format_datetime_df.copy()

# Remove rows from the DataFrame where there is no ascent or descent data
elevation.dropna(subset=['ascent', 'descent'], inplace=True)

# Determine the change in elevation and store it in the change_in_
elevation['change_in_elevation'] = elevation['ascent'] - elevation['descent']

# Output whether the user ran an overall incline or decline on their run
if elevation['change_in_elevation'].sum() > 0:
    elevation_change = 'overall incline'
elif elevation['change_in_elevation'].sum() < 0:
    elevation_change = 'overall decline'
else:
    elevation_change = 'flat'

# Create a Python object (dict)
runner = {
    "number_of_times_over_1km_three_days_in_row": number_of_times_over_1km_three_days_in_row,
    "number_of_weeks_over_10km": number_of_weeks_over_10km,
    "elevation_change": elevation_change
}

# Convert the Python object into JSON
runner_data = json.dumps(runner)
# Print the JSON data to the screen
print(runner_data)
