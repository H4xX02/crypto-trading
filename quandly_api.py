import pandas as pd
import numpy as np
import os
import quandl
import time
import matplotlib.pyplot as plt
from matplotlib import style

## thisisnthappiness

##get alltime daily BTC/USD quotes from Quandl: 

df = quandl.get("BITFINEX/BTCUSD", authtoken="65bn72F_4tCtK9-XHnAu")

## Model validation, calc returns and fast and slow Moving Average: Buy signal if MA_fast > MA_slow

df['returns'] = df['Last'] - df['Last'].shift(1)
df['ma22'] = df['Last'].rolling(window=22,min_periods=0).mean()
df['ma11'] = df['Last'].rolling(window=11,min_periods=0).mean()
df['cum_returns'] = np.cumsum(df['returns'])

z = (df['ma11'] > df['ma22']) & (df['ma11'] != 0)

df['signal'] = z
df['pnl'] = df['returns']*df['signal']
df['cum_returns_ma_cross'] = np.cumsum(df['pnl'])

print(df.tail())

## backtest funtion: clean up!

def backtest(df, ma1, ma2):
	## ma1 = slow moving average
	## ma2 = fast moving average
	df['returns'] = df['Last'] - df['Last'].shift(1)
	df['ma_slow'] = df['Last'].rolling(window=ma1,min_periods=0).mean()
	df['ma_fast'] = df['Last'].rolling(window=ma2,min_periods=0).mean()
	df['cum_returns'] = np.cumsum(df['returns'])

	z = (df['ma_fast'] > df['ma_slow']) & (df['ma11'] != 0)

	df['signal'] = z
	df['pnl'] = df['returns']*df['signal']
	df['cum_returns_ma_cross_x'] = np.cumsum(df['pnl'])

	xox = np.sum(df['pnl'])
	##print(df['cum_returns_ma_cross_x'])
	print(xox)
	return(xox)

print('xxxxxxxxxxxxxxx')

backtest(df, 22, 11)


z1 = [11,22,33,44,55,66,77]
z2 = [11,22,33,44,55,66,77]

q = np.linspace(1,100,100, dtype = 'int')
print(q)

q1 = np.linspace(1,200,100, dtype = 'int')
print(q1)


result_matrix = np.zeros((len(z1),len(z2)),dtype = 'int')

## Run backtest for i & j in z

for i, x1 in enumerate(z1):
	for j, x2 in enumerate(z2):
		back = backtest(df,ma1 = x1, ma2 = x2)
		result_matrix[i,j] = back

print(result_matrix)


