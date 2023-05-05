import datetime as dt
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader as pdr
import os

#GENERATE CSV

# style.use("ggplot")
# startDate = "1/1/2016"
# endDate = "12/31/2016"
# df = pdr.get_data_tiingo("TSLA", start = startDate, end = endDate, api_key="7b8bcbce3ab29ba846ae03b4c37cfe1a8cbae349")

# df.to_csv("tsla.csv")

#READ CSV

df = pd.read_csv("tsla.csv", parse_dates=True, index_col=1)

#print(df.head())

df[["high", "low"]].plot()
plt.show()

