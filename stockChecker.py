#!/usr/bin/env python
import psycopg2
from config import config
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt
from click._compat import raw_input
import pandas as pd

def connect(name, ticker, tickerprice, value):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        print('PostgreSQL database version:')
        cur.execute('insert into public.indicators ')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
	    # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

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
    def rsi(self):
        b=TechIndicators(key=self.api_key2,output_format='json')
        data,meta_data = b.get_rsi(symbol=self.stock_name,interval='daily',time_period=14)
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
if __name__ == "__main__":
    TI=TechnicalIndicators()
    # current_data = TI.current_data
    # print(current_data['01. symbol'])
    # print(current_data['05. price'])
    ema50 = TI.ema(50)
    ema20 = TI.ema(20)
    ema20value = ema20[next(iter(ema20))]['EMA']
    ema50value = ema50[next(iter(ema50))]['EMA']

    # print the most recent value in a time series
    print(ema50value)
    # print(ema_data)