# %% Imports
import string
import math
from src.utils.utils import load_data
from src.constants import *
import pandas as pd
from statsmodels.tsa import seasonal as ssnl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Start exploring the target series (% Silica Concentrate)
SILICA_CONCENTRATE = "% Silica Concentrate"

# %% Load interim data
df = load_data("interim", data_format="pkl")

#%% Describe
df[SILICA_CONCENTRATE].describe() 

#%% Simple line plot
df[SILICA_CONCENTRATE].plot()

#%% Differencing
diff = df[SILICA_CONCENTRATE] - df[SILICA_CONCENTRATE].shift()
diff.plot()

#%% Plot both SLT(LOESS) and naive seasonal decompose 
def decompose_plot(data: pd.DataFrame, freq: string, interval: int):
    data = data.resample(freq).mean().ffill()
    
    decomp_slt = ssnl.STL(data).fit()
    decomp_naive = ssnl.seasonal_decompose(data, model = "multiplicative", extrapolate_trend="freq")
    
    # Plot
    plt.tight_layout()
    fig = plt.figure()
    fig.suptitle(f"SLT & Naive Decompositions (freq={freq})")
    fig.set_figheight(6)
    fig.set_figwidth(10)
    gs = fig.add_gridspec(7, hspace=0.5)
    axs = gs.subplots()
    # Observed
    axs[0].plot(data.index, decomp_slt.observed)
    axs[0].set(ylabel="Observed")
    # Trend
    axs[1].plot(data.index, decomp_slt.trend)
    axs[1].set(ylabel="T SLT")
    axs[2].plot(data.index, decomp_naive.trend)
    axs[2].set(ylabel="T Naive")
    # Seasonal
    axs[3].plot(data.index, decomp_slt.seasonal)
    axs[3].set(ylabel="S SLT")
    axs[4].plot(data.index, decomp_naive.seasonal)
    axs[4].set(ylabel="S Naive")
    # Resid
    axs[5].scatter(data.index, decomp_slt.resid)
    axs[5].set(ylabel="R SLT")
    axs[6].scatter(data.index, decomp_naive.resid)
    axs[6].set(ylabel="R Naive")

    # Change date tick format
    for i in range(7):
        axs[i].xaxis.set_major_locator(mdates.DayLocator(interval=interval))
        axs[i].xaxis.set_major_formatter(mdates.DateFormatter('%d'))

#%% TODO Decomposition in minutes
# decomposition = ssnl.seasonal_decompose(df[SILICA_CONCENTRATE].asfreq('T'), model = "multiplicative", extrapolate_trend="freq")
# decomposition.plot()

#%% Decomposition in hours
size = df[SILICA_CONCENTRATE].size
hour_series = df[SILICA_CONCENTRATE][:math.trunc(size/10)]
decompose_plot(hour_series, "H", 1)

#TODO Zoom to find the period of the hours seasonality 

#%% Decomposition in days full series
decompose_plot(df[SILICA_CONCENTRATE][180*24*5:], "D", 7)

#%% Decomposition in days zoom to get a visual idea of the season period
decompose_plot(df[SILICA_CONCENTRATE][180*24*6:math.trunc(size/4)], "D", 1)

# Looks like a 7 days season

#%% TODO Decomposition in weeks: 20s*3( = 1 min) * 60 ( = 1 huor) * 24 ( = 1 day) * 7 ( = 1 week)
# decomposition = ssnl.seasonal_decompose(df[SILICA_CONCENTRATE], period = 20*3*60*24, model = "multiplicative", extrapolate_trend="freq")
# decomposition.plot()

#%% TODO Decomposition in months

#%% Histogram
#df[SILICA_CONCENTRATE].hist()

#%% TODO
# use pandas express to get some quick insights?
# for each resolution? (seconds, min, hours, days, weeks, months)

# Plot Features Over Time Saving in html files
# n_columns = len(df_raw.axes[1]) - 1

# for i in range(n_columns):
#     series = df_raw.iloc[:,i+1]
#     FILE_NAME_CSV = os.path.join(FIGURES_PATH, f"raw_eda/line/{i}_{series.name}.html")

#     fig = px.line(df_raw, x=df_raw.index, y=series)
#     fig.update_layout(yaxis_title=series.name, xaxis_title="Time")
#     fig.show()
#     plt(fig, filename=FILE_NAME_CSV)