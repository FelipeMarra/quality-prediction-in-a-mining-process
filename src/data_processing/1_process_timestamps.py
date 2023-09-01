# %%
import os
from src.utils.utils import load_data
from src.constants import *
import pandas as pd

# %%
# Load raw data
df_raw = load_data("raw")
df_raw.dtypes

# Processing the data as explored in 
# src/visualization/0_data_raw_eda.py

# %%
# Convert to the 20 in 20s freq
# asfreq wont work in a duplicated index

#skip the 1st as it will ramain with 0 seconds
indexes = df_raw.index.to_series()

hr_counter = 0
g_counter = 0 #global counter
last_idx = indexes[0]

for current_idx in indexes:
    # For each hour (indexes are repeated hourly)
    if(last_idx == current_idx):
        # Add 20s * counter (20 in 20s)
        indexes[g_counter] = indexes[g_counter] + pd.to_timedelta(20 * hr_counter, unit='s')
        hr_counter = hr_counter + 1
    else:
        hr_counter = 1
        last_idx = current_idx

    g_counter = g_counter + 1

#%%
# Replace index
df = df_raw.set_index(indexes)

# %%
# Drop datetimes past 2017-03-29 11:00:00 to remove the part without data
# and the first hour wich also has fewer samples
df = df.loc["2017-03-29 11:00:00":]

df.head()

# %%
# How much info was lost?
print(df.index.size)
print(df_raw.index.size)
lost_percent = (1-(df.index.size / df_raw.index.size))*100

print(f"Lost: {lost_percent}% of the data with the drop")

# %%
# Use forward fill to convert hour 2017-04-10 00:00:00 to 180 samples
df = df.asfreq(freq="20S", method="ffill")

#%%
# Check freq
grouped = df.groupby(pd.Grouper(level="date", axis=0, freq="H")).size()

print(f"The unique num of samples between the hours are: {grouped.unique()}")

#%% 
# Check for duplicated labels
# TODO WHY is it finding duplicated labels????? 
# The asfreq method wodnt even work if that was true
dup_idxs = df.duplicated().where(lambda x: x == True).dropna().index
print("Duplicated indexes: ")
dup_idxs

#%%
# Save dataframe
df.to_pickle(os.path.join(DATA_PATH, "interim", FILE_NAME_PKL))

#%%
# This data will be vizualized at
# src/data_processing/2_silica_concentrate_viz.py