import pandas as pd
import numpy as np
import os
import quandl
import time
import matplotlib.pyplot as plt
from matplotlib import style

## thisisnthappiness

##get alltime daily BTC/USD quotes from Quandl: 

keyFile = open('Authtokens.txt', 'r')
quandl_token = keyFile.readline()


df = quandl.get("BITFINEX/BTCUSD", authtoken= quandl_token)

## Model validation, calculate returns and fast (11) and slow (22) Moving Average: Buy signal if MA_fast > MA_slow, lock in t+1 return

df['returns'] = df['Last'] - df['Last'].shift(+1)
df['ma_slow'] = df['Last'].rolling(window=22,min_periods=0).mean()
df['ma_fast'] = df['Last'].rolling(window=11,min_periods=0).mean()
df['cum_returns'] = np.cumsum(df['returns'])

z = (df['ma_fast'] > df['ma_slow']) & (df['ma_fast'] != 0)

df['signal'] = z

df['pnl'] = df['returns'].shift(-1)*df['signal']
df['cum_returns_ma_cross'] = np.cumsum(df['pnl'])

print(df.tail())
df.to_csv('BTC_MA_Cross.csv')

## backtest funtion: clean up!

def backtest(df, ma1, ma2):
	## ma1 = slow moving average
	## ma2 = fast moving average
	df['returns'] = df['Last'] - df['Last'].shift(+1)
	df['ma_slow'] = df['Last'].rolling(window=ma1,min_periods=0).mean()
	df['ma_fast'] = df['Last'].rolling(window=ma2,min_periods=0).mean()
	df['cum_returns'] = np.cumsum(df['returns'])

	z = (df['ma_fast'] > df['ma_slow']) & (df['ma_fast'] != 0)

	df['signal'] = z
	df['pnl'] = df['returns'].shift(-1)*df['signal']
	df['cum_returns_ma_cross_x'] = np.cumsum(df['pnl'])

	xox = np.sum(df['pnl'])
	##print(df['cum_returns_ma_cross_x'])
	print(xox)
	return(xox)

print('xxxxxxxxxxxxxxx')

backtest(df, 22, 11)


z1 = [22,50,100,125,150,175,200]
z2 = [11,22,33,44,55,66,77]




result_matrix = np.zeros((len(z1),len(z2)),dtype = 'int')

## Run backtest for i & j in z

for i, x1 in enumerate(z1):
	for j, x2 in enumerate(z2):
		back = backtest(df,ma1 = x1, ma2 = x2)
		result_matrix[i,j] = back

print(result_matrix)

print(result_matrix[0,0])

plt.pcolor(z1,z2,result_matrix)
plt.xlabel('MA_long')
plt.ylabel('MA_short');
plt.colorbar();

plt.show()

i,j = np.unravel_index(result_matrix.argmax(),result_matrix.shape)
result_matrix[j,i]

print('opt MA_long %.2f' % z1[i])
print('opt MA_short %.2f' % z2[j])

print(z1[i])
print(z2[j])

backtest(df,z1[i],z2[j])



