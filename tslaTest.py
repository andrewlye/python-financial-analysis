import datetime as dt
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader as pdr
import os

os.environ["IEX_API_KEY"] = "pk_cf3a7cff2abd42f2b9f36061cd5f40e7"

style.use("ggplot")
startDate = "1/1/2010"
endDate = "12/31/2016"
df = pdr.data.DataReader("TSLA", 'iex', start = startDate, end = endDate)
print(df.head())