# %%
import os
from src.utils.utils import load_data
from src.constants import *
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.offline import plot as plt

# %%
# Load raw data
df_raw = load_data("raw")

# %%
df_raw.head()

# %%
df_raw.tail()

# There are date in the same date and hour because some columns were sampled every 20 seconds.
# Others were sampled on a hourly base.

# The second (% Iron Feed) and third (% Silica Feed) columns are quality measures of the iron ore
# pulp right before it is fed into the flotation plant. 

# Column 4 until column 8 (Starch Flow,	Amina Flow, Ore Pulp Flow, Ore Pulp pH, Ore Pulp Density)
# are the most important variables that impact in the ore quality in the end of the process.

# From column 9 until column 22, we can see process data (level and air flow inside the flotation 
# columns), which also impact in ore quality.

# The last two columns (% Iron Concentrate,	% Silica Concentrate) are the final iron ore pulp 
# quality measurement from the lab.

#Target is to predict the last column, which is the % of silica in the iron ore concentrate.

# Q. Is it possible to predict % Silica Concentrate every minute?
# Q. How many steps (hours) ahead can we predict % Silica in Concentrate? This would help engineers
# to act in predictive and optimized way, mitigatin the % of iron that could have gone to 
# tailings.
# Q. Is it possible to predict % Silica in Concentrate whitout using % Iron Concentrate column
# (as they are highly correlated)?

# %%
df_raw.describe()

# %%
df_raw.dtypes

# %% 
# There aren't any null values
print(f"Null values: {df_raw.isnull().any().any()}")

# %%
# Verify sampling rate
sampling_rate_check = all(df_raw.index.to_series().diff()[1:] == np.timedelta64(20, 's')) == True
print(f"Sampling rate check: {sampling_rate_check}")
print()

#%%
# Since 60min * 3x group of 20s will give us the period between 1 hr
# scaterr plot it to investigate the behavior given that there are many
# samples with the same date and hour
# Q. Are the information between hours are been lost?
series = df_raw["Starch Flow"]
print(series)
file_name = os.path.join(FIGURES_PATH, "raw_eda/plot_between_2_hrs-20s_sample.html")
time_spam = 3*60*2-6

fig = px.scatter(df_raw, x=df_raw.index[:time_spam], y=series[:time_spam])
fig.update_layout(yaxis_title=series.name, xaxis_title="Time")
fig.show()
# A. Yes, the plot lib is not subdividing the time between the hours and the
# other libs wont also, so this needs to be fixed

#%%
# Searching for sample freq anomalies
grouped = df_raw.groupby(pd.Grouper(level='date', axis=0, freq='H')).size()

print(f"There unique num of samples between the hours are: {grouped.unique()}, we neeed all hours to have 180")

#%%
# The first hour has 174 samples
print(f"The first hour has {grouped.iloc[0]} samples")

#%%
# Missing data range:
# 2017-03-16 06:00:00
# 2017-03-29 11:00:00 
grouped_0 = grouped[1:].where(lambda x: x == 0).dropna()
print(f"There are {grouped_0.count()} 0 sample hours.")
print(f"They start at {grouped_0.index[0]}, and end at {grouped_0.index[len(grouped_0.index)-1]}")
range = pd.date_range(start="2017-03-16 06:00:00", end="2017-03-29 11:00:00", freq="1H")
print(f"Exploring this range we get unique values: {grouped[range].unique()}")
print(f"And a size of {grouped[range].size} values")

#%%
# Hour w/ 179 samples: 2017-04-10 00:00:00
print(f"The hour 2017-04-10 00:00:00 has {grouped.loc['2017-04-10 00:00:00']} samples")

#%%
# This data will be processed to ajust the timestamps at 
# src/data_processing/1_process_timestamps.py