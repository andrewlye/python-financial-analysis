import bs4 as bs
import datetime as dt
import os
import pandas as pd
import pandas_datareader as pdr
import pickle
import requests

def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, features="lxml")
    table = soup.find('table', {'id':'constituents'})
    tickers = []
    for row in table.findAll('tr') [1:]:
        indexStop = row.findAll('td')[0].text.index('\n')
        ticker = row.findAll('td')[0].text[:indexStop].replace('.','-')
        tickers.append(ticker)
    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
    
    print(tickers)
    return tickers

def get_data_from_tiingo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
    startDate = dt.datetime(2000,1,1)
    endDate = dt.datetime(2022,12,31)

    for ticker in tickers:
        print(ticker)
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = pdr.get_data_tiingo(ticker, start = startDate, end = endDate, api_key="7b8bcbce3ab29ba846ae03b4c37cfe1a8cbae349")
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print("Already have {}".format(ticker))

#get_data_from_tiingo()

def compile_data():
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)
    main_df = pd.DataFrame()
    limit = 11
    for count,ticker in enumerate(tickers):
        if os.path.isfile('stock_dfs/{}.csv'.format(ticker)):
            df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
            df.set_index('date', inplace=True)

            df.rename(columns = {'adjClose':ticker}, inplace=True)
            df.drop(['open', 'high', 'low', 'close', 'volume', 'adjHigh', 'adjLow', 'adjOpen', 'adjVolume', 'divCash', 'splitFactor', 'symbol'], 1, inplace=True)

            if main_df.empty:
                main_df = df
            else:
                main_df = pd.merge(main_df, df, on="date", how='left')
        else:
            print(ticker+" does not exist.")
        
        if count % 10 == 0:
            print(count, ticker)

    print(main_df.head(20))
    main_df.to_csv('sp500_joined_closes.csv')

df1 = pd.read_csv('sp500_joined_closes.csv')
print(df1.tail())