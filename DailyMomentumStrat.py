
import tradingWithPython as twp
import pandas as pd
import numpy as np
import quandl
import matplotlib.pyplot as plt

keyFile = open('Authtokens.txt', 'r')
quandl_token = keyFile.readline()


df = quandl.get("BITFINEX/BTCUSD", authtoken= quandl_token)

print(df.tail())

# df.plot()
# plt.show()

stratData = pd.DataFrame(index = df.index)
stratData['daily_returns'] = df.Last.pct_change()*100
stratData.daily_returns.cumsum().plot()
plt.show()
print('Sharpe buy & hold', twp.sharpe(stratData.daily_returns))

# initialize strategy idx

idx = (stratData.daily_returns<-3).shift(1) #&  (stratData.daily_returns <- 1) # find days that satisfy strategy
idx[0] = False # fill first entry with False due) NaN

stratData['GoLong'] = idx
stratData['pnl'] = 0 # innitialize pnl column with zeros
stratData['pnl'][idx] = stratData['daily_returns'][idx]

print(stratData.tail(30))

print('Sharpe', twp.sharpe(stratData.pnl))

stratData.pnl.cumsum().plot()
plt.show()

# rewrite strategy to a single funtion

def backtest(df, lag1 = -3):							# , lag0 = -1
	'''Function to backtest parameters'''
	stratData = pd.DataFrame(index = df.index)
	stratData['daily_returns'] = df.Last.pct_change()*100

	idx = (stratData.daily_returns < lag1).shift(1) #& (stratData.daily_returns < lag0) # find days that satisfy strategy
	idx[0] = False # fill first entry with False due) NaN
	stratData['GoLong'] = idx
	stratData['pnl'] = 0 # innitialize pnl column with zeros
	stratData['pnl'][idx] = stratData['daily_returns'][idx]

	return stratData['pnl']

# Test of backtest function

pnl = backtest(df)
pnl.cumsum().plot()
print('Sharpe', twp.sharpe(stratData.pnl))
plt.show()

# Scan all possible parameters

par1 = np.linspace(-10,10,30)
lag0 = np.linspace(-10,10,30)

SH = np.zeros(len(par1))

for i, cc in enumerate(par1):
	pnl = backtest(df, lag1 = cc)
	SH[i] = twp.sharpe(pnl)

print(SH)

i = np.unravel_index(SH.argmax(),SH.shape)
SH[i]
print('opt Threshold %.2f' % par1[i])

print(par1[i])

optimized_pnl = backtest(df, par1[i])
print('Sharpe', twp.sharpe(optimized_pnl))
optimized_pnl.cumsum().plot()
plt.show()

print(stratData.daily_returns.sum())
print(optimized_pnl.sum())


