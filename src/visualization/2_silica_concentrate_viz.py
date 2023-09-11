# %% Imports
import string
import math
from src.utils.utils import load_data
from src.constants import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
pd.plotting.register_matplotlib_converters()
from statsmodels.tsa import seasonal as ssnl
from statsmodels.graphics.tsaplots import plot_acf

# %% Load interim data
df = load_data("interim", data_format="pkl")

#%% Start exploring the target series (% Silica Concentrate)
silica = df[SILICA_CONCENTRATE]
SIZE = silica.size

#%% Scatter plot
silica.plot(style=".", figsize=(10,5))

#%% Rolling exponentially weighted mean 
ema_silica = silica.ewm(span=180*48).mean()
orig_vs_ema = pd.DataFrame({"silica": silica, "silica_ema": ema_silica})
orig_vs_ema.plot(figsize=(10,5))

#%% 
orig_vs_ema[:math.ceil(SIZE/4)].plot(figsize=(10,5))

#%%
ema_silica.plot(figsize=(10,5), color="orange")

#%% TODO Rolling win minimum aligned

#%% Describe original silica
silica.describe()

#%% Describe with rolling mean
ema_silica.describe()

#%% ACF ORIGINAl Freq=20S
plot_acf(silica, title="ACF Freq=20S")

#%% ACF Freq=T
plot_acf(silica.resample("T").mean(), title="ACF Freq=T")

#%% "ACF Freq=H"
plot_acf(silica.resample("H").mean(), title="ACF Freq=H")

#%% ACF EMA Freq=H
plot_acf(ema_silica.asfreq("H"), title="ACF EMA Freq=H")

#%% "ACF Freq=D"
plot_acf(silica.resample("D").mean(), title="ACF Freq=D")

#%% ACF EMA Freq=D
plot_acf(ema_silica.asfreq("D"), title="ACF EMA Freq=D")

#%% ACF Freq=W
plot_acf(silica.resample("W").mean(), title="ACF Freq=W")

#%% ACF Freq=M
plot_acf(silica.resample("M").mean(), title="ACF Freq=M")

#%% Line plot & Distribution
def line_and_dist(data, freq = None, line_size=SIZE/10, shift=False, label_int=4):
    data = data.resample(freq).mean() if freq else data
    data = data - data.shift() if shift else data

    silica_label = f"Diff({SILICA_CONCENTRATE})" if shift else f"{SILICA_CONCENTRATE}"
    fig, axs = plt.subplots(2,1)
    freq = freq if freq else "20S"
    fig.suptitle(f"Line (w/ SIZE/10) and Hist (freq={freq}, shift={shift})")
    fig.set_figheight(8)
    axs[0].plot(data[:math.trunc(line_size)])
    axs[0].xaxis.set_major_locator(mdates.DayLocator(interval=label_int))
    axs[0].set_xlabel("dates")
    axs[0].set_ylabel(silica_label)
    axs[1].hist(data)
    axs[1].set_ylabel("Frequency")
    axs[1].set_xlabel(silica_label)

#%% Simple line plot
line_and_dist(silica)
# Seems to show a few days seasonality

#%% Differencing (by every 20s)
#"We difference the data to remove the trend, and this transforms the data to a
# more normally shaped distribution. [...] Most interesting is how a value changes
# from one measurement to the next rather than the value’s actual measurement"
line_and_dist(silica, shift=True)

#TODO Minutes

#%% Differencing by hour
line_and_dist(silica, freq="H", shift=True, label_int=32)

#%% Differencing by days
line_and_dist(silica, freq="D", shift=True, label_int=32)

#%% Differencing by weeks
line_and_dist(silica, freq="W", shift=True, label_int=32)

#%% Differencing by weeks
line_and_dist(silica, freq="M", shift=True, label_int=32)

# Looks like data don't change much over time, and tends twoards the negative side, that is, it
# might be trending down

#%% Plot both SLT(LOESS) and naive seasonal decompose 
def decompose_plot(data: pd.DataFrame, freq: string, interval: int):
    data = data.resample(freq).mean()
    
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

#%% TODO Decomposition in minutes, 20s*3( = 1 min), period = 3 ?
# decomposition = ssnl.seasonal_decompose(silica, period = 3, model = "multiplicative", extrapolate_trend="freq")
# decomposition.plot()

#%% Decomposition in hours
hour_series = silica[:math.trunc(SIZE/10)]
decompose_plot(hour_series, "H", 1)

#TODO Zoom to find the period of the hours seasonality 

#%% Decomposition in days full series
decompose_plot(silica, "D", 7)

#%% Decomposition in days zoom to get a visual idea of the season period
decompose_plot(silica[180*24*6:math.trunc(SIZE/4)], "D", 1)

# Looks like a 7 days season

#%% TODO Decomposition in weeks: 20s*3( = 1 min) * 60 ( = 1 huor) * 24 ( = 1 day) * 7 ( = 1 week)
# decomposition = ssnl.seasonal_decompose(silica, period = 3*60*24, model = "multiplicative", extrapolate_trend="freq")
# decomposition.plot()

#%% TODO Decomposition in months

#%% TODO
# The shortcoming with seasonal decomposition models is that it does not capture how a season might
# change through time. For example, the characteristics of a week of electricity demand in the 
# summer is much different than the winter. This method will determine an average seasonal pattern 
# and leave the remaining information in the residuals. So given your characteristics vary by day
# of week (mentioned in your other post), this won't capture that.

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
# %%
