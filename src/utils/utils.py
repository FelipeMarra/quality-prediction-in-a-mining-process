import os
import string
import pandas as pd
from src.constants import *

# Starts with DATA_PATH (path to the data folder) and auto complets with file_name,
# wich defaluts to "MiningProcess_Flotation_Plant_Database.csv"
# So to acess the raw data, path_from_data should be "raw". The function will then
# return a dataframe read from DATA_PATH/raw/file_name
def load_data(path_from_data: string, file_name = FILE_NAME, sort = True, date_as_index = True) -> pd.DataFrame:

    index_col = "date" if date_as_index else None

    path = os.path.normpath(DATA_PATH + os.sep + path_from_data + os.sep + file_name)

    df = pd.read_csv(path, sep=",", decimal=",", index_col=index_col,
                     parse_dates=['date'])
    
    if sort:
        df.sort_index(inplace=True)

    return df