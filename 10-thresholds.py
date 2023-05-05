import numpy as np
import pandas as pd
import pickle

def process_data_for_labels(ticker):
    hm_days = 7 #how many days into the future do we have to make/lose x%
    df = pd.read_csv('sp500_joined_closes.csv', index_col=0)
    tickers = df.columns.values.tolist()
    df.fillna(0, inplace=True)

    for i in range(1, hm_days+1):
        df['{}_{}d'.format(ticker,i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker] #MMM_2d, stock value day 2 into the future

    df.fillna(0, inplace=True)
    return tickers, df

def buy_sell_hold(*args): #args pass any num of non-key worded variables
    cols = [c for c in args]
    requirement = 0.02 #% change requirement
    for col in cols:
        if col > requirement: #buy
            return 1
        if col < -requirement: #sell
            return -1
    return 0 #hold