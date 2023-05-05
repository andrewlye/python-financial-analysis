import datetime as dt
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import style
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader as pdr
from pandas.plotting import register_matplotlib_converters

style.use("ggplot")

register_matplotlib_converters()

df = pd.read_csv("tsla-2010-2016.csv", parse_dates=True, index_col=1)
#df['100ma'] = df['adjClose'].rolling(window=100, min_periods=0).mean() #100 moving average
#df.dropna(inplace=True) #drop all n/a rows, inplace

df_ohlc = df['adjClose'].resample('10D').ohlc()
df_volume = df['volume'].resample('10D').sum()
df_ohlc.reset_index(inplace=True)
df_ohlc['date'] = df_ohlc['date'].map(mdates.date2num)

ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
ax1.xaxis_date()

candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, color='lightblue')

plt.show()