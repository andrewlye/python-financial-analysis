import datetime as dt
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader as pdr
from pandas.plotting import register_matplotlib_converters

style.use("ggplot")
register_matplotlib_converters()

df = pd.read_csv("tsla.csv", parse_dates=True, index_col=1)
df['100ma'] = df['adjClose'].rolling(window=100, min_periods=0).mean() #100 moving average
#df.dropna(inplace=True) #drop all n/a rows, inplace
print(df.head())

ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)

ax1.plot(df.index, df["adjClose"])
ax1.plot(df.index, df["100ma"])
ax2.bar(df.index, df["volume"])

plt.show()