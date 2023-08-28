# %%
import os
from src.utils.utils import load_data
from src.constants import *
import pandas as pd
import numpy as np

# %%
# Load raw data
df_raw = load_data("raw")
df_raw.head()

# Processing the data as explored in 
# src/visualization/0_data_raw_eda.py

# %%
# Convert to the 20 in 20s freq
# asfreq wont work in a duplicated index
#skip the 1st as it will ramin with 0 seconds
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
        hr_counter = 0
        last_idx = current_idx

    g_counter = g_counter + 1

# %%
# Drop datetimes past 2017-03-29 11:00:00 to remove the part without data
# and the first hour wich also has fewer samples
df_droped = df_raw.loc["2017-03-29 11:00:00":]
df_droped.head()

# %%
# Use foward fill to convert hour 2017-04-10 00:00:00 to 180 samples
# Get last row in that hour
# np_ffill = df_droped.loc["2017-04-10 00:00:00"].to_numpy()
# ffill_len = len(np_ffill)
# np_ffill = np.append(np_ffill, np_ffill[ffill_len-1])
# row_ffill = [tuple(t) for t in np_ffill[0]]
#df_ffill.head()
#row_ffill
# Inserd it again 


# %%
# TODO: take the avarage by minutes in the data_processing folder