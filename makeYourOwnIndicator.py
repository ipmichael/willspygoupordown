#!/usr/bin/env python
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from click._compat import raw_input
import json

with open('SPY_1min_intraday.json') as timeSeriesFile:
    timeSeriesJson = json.load(timeSeriesFile)
    tsData = timeSeriesJson['Time Series (1min)']
    for p in sorted(tsData.keys()):
        print('Timestamp: ' + p)
        datapoint = tsData[p]
        print('Open: '+ datapoint['1. open'])
        print('Close: '+ datapoint['4. close'])
        print('Volume: '+ datapoint['5. volume'])

with open('EMA20_1min_intraday.json') as ema20File:
    ema20Json = json.load(ema20File)
    ema20Data = ema20Json['Technical Analysis: EMA']
    # for p in ema20Data:
    #     print('Timestamp: ' + p)
    #     print('EMA20: ' + ema20Data[p]['EMA'])

with open('EMA40_1min.json') as ema40File:
    ema40Json = json.load(ema40File)
    ema40Data = ema40Json['Technical Analysis: EMA']

class DataPoint:
    def __init__(self, label, value):
        self.label=label
        self.value=value

class TechnicalIndicators:
    def __init__(self):
        self.api_key1= 'TCVGV5C9L0I7OMG0'
        self.api_key2= 'GOUDK5Y427GJU3B9'
        self.api_key3= 'KMOA5YH5JT2Z2A1B'
        self.stock_name='SPY'
        # self.macd_data=self.macd()
        # self.rsi_data=self.rsi()
        # self.bbands_data=self.bbands()
        # self.current_data=self.current()
        # self.sma_data=self.sma()
        # self.ema_data=self.ema()
    def question(self):
        stock_name=raw_input("Enter stock name:")
        return stock_name
    def macd(self):
        a = TechIndicators(key=self.api_key2, output_format='json')
        data, meta_data = a.get_macd(symbol=self.stock_name,interval='daily')
        return data
    def rsi(self, tp):
        b=TechIndicators(key=self.api_key3,output_format='json')
        data,meta_data = b.get_rsi(symbol=self.stock_name,interval='1min',time_period=tp,series_type='close')
        return data
    def bbands (self):
        c=TechIndicators(key=self.api_key2,output_format='json')
        data,meta_data=c.get_bbands(symbol=self.stock_name)
        return data
    def sma(self):
        d= TechIndicators(key=self.api_key2, output_format='json')
        data, meta_data = d.get_sma(symbol=self.stock_name,time_period=30)
        return data
    def ema(self, tp):
        e=TechIndicators(key=self.api_key2,output_format='json')
        data, meta_data = e.get_ema(symbol=self.stock_name,interval='1min',time_period=tp,series_type='close')
        return data
    def current(self):
        z=TimeSeries(key=self.api_key1,output_format='json')
        data,meta_data=z.get_quote_endpoint(symbol=self.stock_name)
        return data
    def timeSeries(self, interval, outputsize):
        ts=TimeSeries(key=self.api_key3)
        data,meta_data=ts.get_intraday(symbol=self.stock_name,interval=interval,outputsize=outputsize)
        return data
    def getStockName(self):
        return self.stock_name

if __name__ == "__main__":
    print('that is it')
    # print(timeSeriesData)
    # TI=TechnicalIndicators()
    # current_data = TI.current()
    # symbol = current_data['01. symbol']
    # currentPrice = float(current_data['05. price'])

    # timeSeriesData = TI.timeSeries('1min','full')

    # onePoint = timeSeriesData['2020-07-13 19:59:00']
    # print(onePoint)


    # emaSlow = TI.ema(20)
    # emaFast = TI.ema(10)
    # emaFastValue = float(emaFast[next(iter(emaFast))]['EMA'])
    # emaSlowValue = float(emaSlow[next(iter(emaSlow))]['EMA'])
    # emaPrediction = round((emaFastValue-emaSlowValue)*10000/currentPrice,2)

    # rsi14 = TI.rsi(14)
    # rsi2 = TI.rsi(2)
    # rsi14value = float(rsi14[next(iter(rsi14))]['RSI'])
    # rsi2value = float(rsi2[next(iter(rsi2))]['RSI'])
    # rsiPrediction = round((50-rsi2value)/10,2)

    # rsiEmaScore = round(emaPrediction + rsiPrediction,2)
    # print(rsiEmaScore)