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
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf

# %% Load interim data
df = load_data("interim", data_format="pkl")

#%% Start exploring the target series (% Silica Concentrate)
silica = df[SILICA_CONCENTRATE]
SIZE = silica.size

############ Summary & Smoothing #####################################################
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

############ Stationarity #####################################################
#%% Stationarity
size = math.ceil(SIZE*0.5)
print(f"apply adfuller on {silica[size:].size} data points")
print(adfuller(silica[size:]))
# the series is stationary

############ Autocorrelation Function ##########################################
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

############ Differencing Distribution ########################################
#%% Line plot & Distribution
def line_and_dist(data, freq = None, shift=False, interval=4, bins=None):
    data = data.resample(freq).mean() if freq else data
    # current - next (shift increases the indexes)
    data = data - data.shift() if shift else data

    silica_label = f"Diff({SILICA_CONCENTRATE})" if shift else f"{SILICA_CONCENTRATE}"
    plt.tight_layout()
    fig, axs = plt.subplots(2,1)
    freq = freq if freq else "20S"
    fig.suptitle(f"Freq={freq}, Shift={shift})", y=0.92)
    fig.set_figheight(8)
    axs[0].plot(data)
    axs[0].xaxis.set_major_locator(mdates.DayLocator(interval=interval))
    axs[0].set_xlabel("dates")
    axs[0].set_ylabel(silica_label)
    axs[1].hist(data, bins=bins)
    axs[1].set_ylabel("Frequency")
    axs[1].set_xlabel(silica_label)

#%% Simple line plot
line_and_dist(silica, interval=32)

#%% Differencing (by every 20s)
#"We difference the data to remove the trend, and this transforms the data to a
# more normally shaped distribution. [...] Most interesting is how a value changes
# from one measurement to the next rather than the value’s actual measurement"

line_and_dist(silica, shift=True, interval=40, bins=100)

#%% Differencing by hour
line_and_dist(silica, freq="T", shift=True, interval=32, bins=100) 

#%% Differencing by hour
line_and_dist(silica, freq="H", shift=True, interval=32)

#%% Differencing by days
line_and_dist(silica, freq="D", shift=True, interval=32)

#%% Differencing by weeks
line_and_dist(silica, freq="W", shift=True, interval=32)

#%% Differencing by weeks
line_and_dist(silica, freq="M", shift=True, interval=32)

# Looks like data don't change much over time, and tends twoards the negative side, that is, it
# might be trending down

############ Decomposition #################################################
#%% Plot both SLT(LOESS) and naive seasonal decompose
#TODO pegar o resultado E DEPOIS dar split pra dar zoom
def decompose_plot(data: pd.DataFrame, freq:string, interval=1, comments=""): 
    # Since seasonal_decompose can't hadle S, T, W and M, 
    # we resample and set the period to the smallest one
    data = data.resample(freq).mean()
    if freq in ["S", "5T", "W", "M"]:
        decomp_naive = ssnl.seasonal_decompose(data, 
                                               period = 2,
                                               model = "multiplicative", 
                                               extrapolate_trend = "freq")
        decomp_slt = ssnl.STL(data, period=2).fit()
    # Otherwise it's preferible to mantain the statsmodels support to pd labels
    else:
        decomp_naive = ssnl.seasonal_decompose(data, 
                                               model = "multiplicative", 
                                               extrapolate_trend="freq")
        decomp_slt = ssnl.STL(data).fit()

    # Plot
    plt.tight_layout()
    fig = plt.figure()
    fig.suptitle(f"SLT & Naive Decompositions (freq={freq}) {comments}")
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
    #TODO sera q fica melhor como linha ao invés de scatter ??????
    axs[5].scatter(data.index, decomp_slt.resid)
    axs[5].set(ylabel="R SLT")
    axs[6].scatter(data.index, decomp_naive.resid)
    axs[6].set(ylabel="R Naive")

    # Change date tick format
    for i in range(7):
        axs[i].xaxis.set_major_locator(mdates.DayLocator(interval=interval))
        axs[i].xaxis.set_major_formatter(mdates.DateFormatter('%d'))

#%% Decomposition in minutes
decompose_plot(silica[:math.trunc(SIZE*0.008)], freq="5T", comments="1% of data")

#%% Decomposition in hours
decompose_plot(silica[:math.trunc(SIZE/10)], freq="H", comments="10% of data")

#%% Decomposition in hours: Zoom to get a visual idea of the season period
decompose_plot(silica[:math.trunc(SIZE/4)-180*24*30], freq="H", comments="ZOOM")

#%% Decomposition in days full series
decompose_plot(silica, freq="D", interval=7)

#%% Decomposition in days: Zoom to get a visual idea of the season period
decompose_plot(silica[:math.trunc(SIZE/4)-180*24*6], freq="D", comments="ZOOM")
# Looks like a 7 days season

#%% Decomposition in weeks full series
decompose_plot(silica, freq="W", interval=7)

#%% Decomposition in weeks: Zoom to get a visual idea of the season period
decompose_plot(silica[:math.trunc(SIZE/2)-180*24*30], freq="W", interval=2, comments="ZOOM")

#%% Decomposition in months full series
decompose_plot(silica, freq="M", interval=7)