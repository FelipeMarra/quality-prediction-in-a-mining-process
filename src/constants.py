import os

# Paths
DATA_PATH = os.path.normpath(os.getcwd() + os.sep + os.pardir + os.sep + os.pardir + "/data")
FILE_NAME_CSV = "MiningProcess_Flotation_Plant_Database.csv"
FILE_NAME_PKL = "MiningProcess_Flotation_Plant_Database.pkl"
REPORTS_PATH = os.path.normpath(os.getcwd() + os.sep + os.pardir + os.sep + os.pardir + "/reports")
FIGURES_PATH = os.path.join(REPORTS_PATH, "figures")