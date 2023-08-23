# %%
import os
import pandas as pd
import string
import numpy as np

# %%
# Load raw data

def load_raw_data(path: string) -> pd.DataFrame:
    """
    Load csv data using pandas and return a dataframe
    """

    df = pd.read_csv(path, sep=",", decimal=",", index_col='date',
                     parse_dates=['date'])

    return df

path =  os.path.normpath(os.getcwd() + os.sep + os.pardir + os.sep + os.pardir + "/data")
final_path = os.path.join(path, "raw/MiningProcess_Flotation_Plant_Database.csv")
df_raw = load_raw_data(path=final_path)


# %%
df_raw.head(5)

# %%
df_raw.tail(5)

# There are date in the same date and hor becouse some columns were sampled every 20 seconds.
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
