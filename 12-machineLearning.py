from collections import Counter
import numpy as np
import pandas as pd
import pickle
from sklearn import svm, neighbors #svm for support vector machine, cross_validation to create training and testing samples
from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingClassifier, RandomForestClassifier #use many classifiers and vote on which is best, learn these!


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

def extract_featuresets(ticker):
    tickers, df = process_data_for_labels(ticker)

    df['{}_target'.format(ticker)] = list(map(buy_sell_hold,
                                              df['{}_1d'.format(ticker)],
                                              df['{}_2d'.format(ticker)],
                                              df['{}_3d'.format(ticker)],
                                              df['{}_4d'.format(ticker)],
                                              df['{}_5d'.format(ticker)],
                                              df['{}_6d'.format(ticker)],
                                              df['{}_7d'.format(ticker)]
                                              ))
    vals = df['{}_target'.format(ticker)].values.tolist()
    str_vals = [str(i) for i in vals]
    print('Data spread:', Counter(str_vals))
    df.fillna(0, inplace=True) #replace prior NAs with 0

    df = df.replace([np.inf, -np.inf], np.nan) #replace infinite % changes (from 0 to something) with nan
    df.dropna(inplace=True)

    df_vals = df[[ticker for ticker in tickers]].pct_change()
    df_vals = df_vals.replace([np.inf, -np.inf], 0)
    df_vals.fillna(0, inplace=True)

    X = df_vals.values #capital X = feature sets (things that describe targets, price changes, % changes, etc.), y = labels (target)
    y = df['{}_target'.format(ticker)].values

    return X, y, df


def do_ml(ticker):
    X, y, df = extract_featuresets(ticker)

    X_train, X_test, y_train, y_test = train_test_split(X,
                                                        y,
                                                        test_size = 0.25,
                                                        random_state=42)
    
    #clf = neighbors.KNeighborsClassifier()
    #use multiple classifiers to find the best one, list of tuples of classifiers
    clf = VotingClassifier([('lsvc', svm.LinearSVC()),
                            ('knn', neighbors.KNeighborsClassifier()),
                            ('rfor', RandomForestClassifier())])
    clf.fit(X_train, y_train)
    confidence = clf.score(X_test, y_test)
    print('Accuracy: ', confidence)
    predictions = clf.predict(X_test)

    print('Predicted spread:', Counter(predictions)) #check the predictions we are making

    return confidence

do_ml('TSLA')


