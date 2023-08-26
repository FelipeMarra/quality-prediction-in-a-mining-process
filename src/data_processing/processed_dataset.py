# %%
import os
import pandas as pd
import string

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