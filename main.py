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

# Filter out runs <= 1km
# This DataFrame will be used to see if the user ran > 1km in a single run 3 days in a row
# greater_one_kilometer_run_df = all_runs_df.loc[all_runs_df['distance'] > 1]
# print(greater_one_kilometer_run_df)

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

runner = {
    "number_of_weeks_over_10km": number_of_weeks_over_10km
}

runner_data = json.dumps(runner)
print(runner_data)

# Determine the difference between days. If the difference is not 0, then drop those rows from the DataFrame

# For the "test" user w/ user_id 72eff89c74cc57178e02f103187ad579, the first run occurred on a Thursday (2015-09-10) and
# the last run occurred on a Wednesday (2018-04-11)
