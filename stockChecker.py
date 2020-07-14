#!/usr/bin/env python
import psycopg2
from config import config
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt
from click._compat import raw_input
import pandas as pd

def writeToDB(cursor, name, ticker, tickerprice, value):
    """ Write to the PostgreSQL database server """
    sql = f'insert into public.indicators(name,ticker,tickerprice,value) VALUES(\'{name}\',\'{ticker}\',{tickerprice},{value});'
    print(sql)
    cursor.execute(sql)

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
    def getStockName(self):
        return self.stock_name

if __name__ == "__main__":
    conn = None
    TI=TechnicalIndicators()
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # getLastTickerpriceSQL = f'select tickerprice from public.indicators where ticker = \'{TI.getStockName()}\' order by time desc limit 1;'
        # print(getLastTickerpriceSQL)
        # cur.execute(getLastTickerpriceSQL)
        # lastTickerprice = cur.fetchone()
        # print(f'Last tickerprice for {TI.getStockName()}: {lastTickerprice}')

        current_data = TI.current()
        symbol = current_data['01. symbol']
        currentPrice = float(current_data['05. price'])

        emaSlow = TI.ema(20)
        emaFast = TI.ema(10)
        emaFastValue = float(emaFast[next(iter(emaFast))]['EMA'])
        emaSlowValue = float(emaSlow[next(iter(emaSlow))]['EMA'])
        emaPrediction = round((emaFastValue-emaSlowValue)*10000/currentPrice,2)

        writeToDB(cur, "EMA", symbol, currentPrice, emaPrediction)

        rsi14 = TI.rsi(14)
        rsi2 = TI.rsi(2)
        rsi14value = float(rsi14[next(iter(rsi14))]['RSI'])
        rsi2value = float(rsi2[next(iter(rsi2))]['RSI'])
        rsiPrediction = round((50-rsi2value)/10,2)

        writeToDB(cur, "RSI", symbol, currentPrice, rsiPrediction)

        rsiEmaScore = round(emaPrediction + rsiPrediction,2)

        writeToDB(cur, "EMA-RSI", symbol, currentPrice, rsiEmaScore)

        # close the communication with the PostgreSQL
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')