# %% Imports
from src.utils.utils import load_data
from src.constants import *
import pandas as pd
pd.plotting.register_matplotlib_converters()
from pandas_profiling import ProfileReport
import plotly.express as px
from statsmodels.tsa.stattools import adfuller

#%% Load interim data
df = load_data("interim", data_format="pkl")

############ Overview w/o preprocessing ##########################################
#%% Use pandas express to get some quick insights
profile = ProfileReport(df)

profile.to_file(os.path.join(REPORTS_PATH,"profile_report_no_pre.html"))
# % Silica Concentrate is highly overall negatively correlated 
# with % Iron Concentrate. But the rest of the data isn't normalized

#%% Plot features saving in html files
n_columns = len(df.axes[1]) - 1

for i in range(n_columns):
    series = df.iloc[:,i+1]
    FILE_NAME_CSV = os.path.join(FIGURES_PATH, f"{i}_{series.name}.html")

    fig = px.line(df, x=df.index, y=series)
    fig.update_layout(yaxis_title=series.name, xaxis_title="Time")
    fig.write_html(FILE_NAME_CSV)

############### Stationarity ##########################################################
#%%
print(df.shape)

#%%
for i in range(df.shape[1]):
    if i > 2:
        print(adfuller(df.iloc[:,i])[1])
        if adfuller(df.iloc[:,i])[1] > 0.05:
            print('{} has p value > 0.05'.format(df.columns.values[i]))

############### Detrend ##############################################################


############### Normalize ############################################################
#%% TODO Normalize data skiping % wich is already normalized i guess
#    *TODO normal plot?
#    *TODO generate report again
#    *TODO generate correlations
#    *TODO generate causality

############### Correlation ##########################################################

############### Causality ############################################################