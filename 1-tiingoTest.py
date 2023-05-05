import datetime as dt
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader as pdr
import os

style.use("ggplot")
startDate = "1/1/2000"
endDate = "12/31/2022"
df = pdr.get_data_tiingo("PEAK", start = startDate, end = endDate, api_key="7b8bcbce3ab29ba846ae03b4c37cfe1a8cbae349")

print(df.head())