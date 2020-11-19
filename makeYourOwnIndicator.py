#!/usr/bin/env python
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from click._compat import raw_input
import json

print('Loading...')

with open('EMA20_1min_intraday.json') as ema20File:
    ema20Json = json.load(ema20File)
    ema20Data = ema20Json['Technical Analysis: EMA']
    # for p in ema20Data:
    #     print('Timestamp: ' + p)
    #     print('EMA20: ' + ema20Data[p]['EMA'])

with open('EMA40_1min.json') as ema40File:
    ema40Json = json.load(ema40File)
    ema40Data = ema40Json['Technical Analysis: EMA']

with open('RSI14_1min.json') as rsi14File:
    rsi14Json = json.load(rsi14File)
    rsi14Data = rsi14Json['Technical Analysis: RSI']
    # for p in rsi14Data:
    #     print('Timestamp: ' + p)
    #     print('EMA20: ' + rsi14Data[p]['RSI'])

with open('ADX14_1min.json') as adx14File:
    adx14Json = json.load(adx14File)
    adx14Data = adx14Json['Technical Analysis: ADX']

with open('BBANDS20_1min.json') as bbands20File:
    bbands20Json = json.load(bbands20File)
    bbands20Data = bbands20Json['Technical Analysis: BBANDS']

with open('MACD12_26_1min.json') as MACD12_26_1min:
    macdJson = json.load(MACD12_26_1min)
    macdData = macdJson['Technical Analysis: MACD']

with open('OBV_1min.json') as obvFile:
    obvJson = json.load(obvFile)
    obvData = obvJson['Technical Analysis: OBV']

with open('SPY_1min_intraday.json') as timeSeriesFile:
    timeSeriesJson = json.load(timeSeriesFile)
    tsData = timeSeriesJson['Time Series (1min)']
    # for p in sorted(tsData.keys()):
    #     print('Timestamp: ' + p)
    #     datapoint = tsData[p]
    #     print('Open: '+ datapoint['1. open'])
    #     print('Close: '+ datapoint['4. close'])
    #     print('Volume: '+ datapoint['5. volume'])

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

def normalize(ary):
    amin, amax = min(ary), max(ary)
    for i, val in enumerate(ary):
        ary[i] = (2*(val-amin) / (amax-amin) - 1)
    return ary

def posNormalize(ary):
    amin, amax = min(ary), max(ary)
    for i, val in enumerate(ary):
        ary[i] = (val-amin) / (amax-amin)
    return ary

if __name__ == "__main__":
    quoteList = []
    ema20List = []
    ema40List = []
    rsi14List = []
    adx14List = []
    macdList = []
    obvList = []
    for ts in sorted(tsData.keys()):
        indicatorCount = 0
        dateKey = ts[0:16]
        # print('For timestamp '+dateKey)
        closeValue = tsData[ts]['4. close']
        # print('Close: ' + closeValue)

        if(ema20Data.get(dateKey, 'none') != 'none'):
            indicatorCount+=1
            ema20Value = ema20Data[dateKey]['EMA']
            # print('EMA20: ' + ema20Value)
            ema20Pred = float(ema20Value) - float(closeValue)
            # print('EMA20 prediction: ' + str(ema20Pred))
        if(ema40Data.get(dateKey, 'none') != 'none'):
            indicatorCount+=1
            ema40Value = ema40Data[dateKey]['EMA']
            # print('EMA40: ' + ema40Value)
            ema40Pred = float(ema40Value) - float(closeValue)
            # print('EMA40 prediction: ' + str(ema40Pred))
        if(rsi14Data.get(dateKey, 'none') != 'none'):
            indicatorCount+=1
            rsi14Value = rsi14Data[dateKey]['RSI']
            # print('RSI14: ' + rsi14Value)
            rsi14Pred = 50-float(rsi14Value)
            # print('RSI14 prediction: ' + str(rsi14Pred))
        if(adx14Data.get(dateKey, 'none') != 'none'):
            indicatorCount+=1
            adx14Value = adx14Data[dateKey]['ADX']
            # print('ADX14: ' + adx14Value)
        if(macdData.get(dateKey, 'none') != 'none'):
            indicatorCount+=1
            macdValue = macdData[dateKey]['MACD_Signal']
            # print('MACD_SIGNAL: ' + macdValue)
        if(obvData.get(dateKey, 'none') != 'none'):
            indicatorCount+=1
            obvValue = obvData[dateKey]['OBV']
            # print('OBV: ' + obvValue)

        if(indicatorCount == 6):
            quoteList.append(float(closeValue))
            ema20List.append(ema20Pred)
            ema40List.append(ema40Pred)
            rsi14List.append(rsi14Pred)
            adx14List.append(float(adx14Value))
            macdList.append(float(macdValue))
            obvList.append(float(obvValue))
        # print('')
    normObvList = normalize(obvList)
    normEMA20 = normalize(ema20List)
    normEMA40 = normalize(ema40List)
    normRSI14 = normalize(rsi14List)
    normADX14 = normalize(adx14List)
    normMACD = normalize(macdList)

    print('Enter weights for technical indicators')
    predWeights = [0,0,0,0,0,0]
    predWeights[0]=raw_input("EMA20: ")
    predWeights[1]=raw_input("EMA40: ")
    predWeights[2]=raw_input("RSI14: ")
    predWeights[3]=raw_input("ADX14: ")
    predWeights[4]=raw_input("MACD: ")
    predWeights[5]=raw_input("OBV: ")

    numCorrect = 0

    for i, val in enumerate(quoteList):
        if(i > 0):
            predList = []
            prev = i-1
            delta = quoteList[i] - quoteList[prev]
            predList.append(normEMA20[prev])
            predList.append(normEMA40[prev])
            predList.append(normRSI14[prev])
            predList.append(normADX14[prev])
            predList.append(normMACD[prev])
            predList.append(normObvList[prev])

            # ema20Pred = normEMA20[prev]
            # ema40Pred = normEMA40[prev]
            # rsi14Pred = normRSI14[prev]
            # adx14Pred = normADX14[prev]
            # macdPred = normMACD[prev]
            # obvPred = normObvList[prev]

            sumPred = 0
            for j, pred in enumerate(predList):
                sumPred += pred * float(predWeights[j])

            if((delta >= 0 and sumPred > 0) or (delta < 0 and sumPred < 0)):
                numCorrect+=1
            # print('Delta: ' + str(delta))
            # print('RSI prediction: ' + str(normRSI14[prev]))

    accuracy = round(100 * float(numCorrect) / float(len(quoteList)),2)
    print('Your custom indicator accuracy: ' + str(accuracy)+ '%')
