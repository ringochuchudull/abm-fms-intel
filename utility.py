import numpy as np
import pandas as pd


BUY  = 0
SELL = 1
HOLD = -1

maxP = 2000
minP = 1

INFINITY = float('inf')
draft_param = 0.3

NO_ACTION = (None, None, None, None)

# A function returning a True with Probability
def probabilityGenerator(boundary=0.25):
    a = np.random.uniform(low=0, high=1)
    if a < boundary:
        return True
    return False

def saveToCSV(marketList):
    import csv

    open1 = marketList[0]
    close = marketList[-1]
    high = max(marketList)
    low = min(marketList)

    csv_columns = ['OPEN','CLOSE','HIGH', 'LOW']
    dict_data = [{'OPEN':open1, 'CLOSE':close, 'HIGH':high, 'LOW':low}]
    try:
        with open('LOGDATA.csv', 'a') as csvfile:
            writer = csv.DictWriter(csvfile , fieldnames=csv_columns)
            #writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError:
        print("I/O error") 

def plotCandleGraph(file='LOGDATA.csv'):
    import plotly
    plotly.tools.set_credentials_file(username='ringochu1997', api_key='XaoFk2TtUzLwKdNAn4vU')
    import plotly.plotly as py
    import plotly.graph_objs as go

    df = pd.read_csv(file)
    open1, close1, high1, low1 = df['OPEN'], df['CLOSE'], df['HIGH'], df['LOW']

    #print(open1, close1, high1, low1)
    trace = go.Candlestick(
                    open=open1,
                    high=high1,
                    low=low1,
                    close=close1)
    data = [trace]
    py.iplot(data, filename='Intel-fake-market')

def PickLastClosePrice(file='LOGDATA.csv'):
    df = pd.read_csv(file)
    yesterday = df['CLOSE']
    print(yesterday)
    yesterday_closed = yesterday.iloc[-1]
    print(yesterday_closed)
    return yesterday_closed

def randomNumberGenerator(l,r):
    return np.random.uniform(low=l, high=r)

if __name__ == '__main__':
    plotCandleGraph()
    PickLastClosePrice()