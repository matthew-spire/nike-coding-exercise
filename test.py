# Define the necessary imports
import glob
import json
import os

import pandas as pd

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

# Accept as input a single user id
user_id = input("Enter user id: ")

# Create a DataFrame filtered using the inputted user_id
user_df = df.loc[user_id]

# Filter out non-run activities
run_df = user_df.loc[user_df['type'] == 'run']
# print(run_df)

# Create a copy of the user_df
format_datetime_df = run_df.copy()

# Convert the start and end to a datetime format
format_datetime_df[['start', 'end']] = format_datetime_df[['start', 'end']].apply(pd.to_datetime, errors='coerce')
# The following is code that may or may not be needed later, but should be deleted before submission
# format_time_user_df.loc[:, ['start', 'end']] = format_time_user_df.loc[:, ['start', 'end']].apply(pd.to_datetime, errors='coerce')
# format_time_user_df['start'] = format_time_user_df['start'].dt.date
# cols = ['start', 'end']
# format_time_user_df[cols] = format_time_user_df[cols].apply(lambda x: pd.to_datetime(x, unit='ms').dt.normalize())

# Sort by the start date/time in ascending
format_datetime_df = format_datetime_df.sort_values(by='start', ascending=True)

# Print the data to the screen
print(format_datetime_df)
