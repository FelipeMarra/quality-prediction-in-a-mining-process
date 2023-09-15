import os
import string
import pandas as pd
from src.constants import *

# Path starts with DATA_PATH (constant to the data folder) and auto complets with FILE_NAME_CSV,
# wich defaluts to "MiningProcess_Flotation_Plant_Database.csv"
# So to acess the raw data, path_from_data should be "raw". The function will then
# return a dataframe read from DATA_PATH/raw/FILE_NAME_CSV
def load_data(path_from_data: string, data_format = "csv", sort = True, date_as_index = True) -> pd.DataFrame:

    index_col = "date" if date_as_index else None

    file_name = FILE_NAME_CSV if data_format == "csv" else FILE_NAME_PKL

    path = os.path.normpath(DATA_PATH + os.sep + path_from_data + os.sep + file_name)

    if data_format == "csv" and path_from_data == "raw":
        df = pd.read_csv(path, sep=",", decimal=",", index_col=index_col, parse_dates=['date'])
    elif data_format == "csv" and path_from_data != "raw":
        df = pd.read_csv(path, sep=",", decimal=",")
    else:
        df = pd.read_pickle(path)
    
    if sort:
        df.sort_index(inplace=True)

    return df