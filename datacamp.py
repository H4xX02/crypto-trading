## https://www.datacamp.com/courses/importing-managing-financial-data-in-python
## https://www.datacamp.com/courses/intro-to-python-for-data-science
## https://www.datacamp.com/community/tutorials/finance-python-trading#gs.vER0FcI

import pandas_datareader as pdr
import datetime 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



## aapl = pdr.get_data_yahoo('AAPL', 
##                          start=datetime.datetime(2006, 10, 1), 
##                          end=datetime.datetime(2012, 1, 1))

## print(aapl.describe())
## print(aapl.tail())

## aapl.to_csv('data/aapl_ohlc.csv')
aapl = pd.read_csv('data/aapl_ohlc.csv', header = 0, index_col = 'Date', parse_dates = True)

print(aapl.index)
print(aapl.columns)

ts = aapl['Close'][-10:]

print(ts)

print(type(ts))

# Inspect the first rows of November-December 2006
print(aapl.loc[pd.Timestamp('2006-11-01'):pd.Timestamp('2006-12-31')].head())

# Inspect the first rows of 2007 
print(aapl.loc['2007'].head())

# Inspect November 2006
print(aapl.iloc[22:43])

# Inspect the 'Open' and 'Close' values at 2006-11-01 and 2006-12-01
print(aapl.iloc[[22,43], [0, 3]])

# Sample 20 rows
sample = aapl.sample(20)
print(sample)

# Resample to monthly level 
monthly_aapl = aapl.resample('M').mean()
print(monthly_aapl)

print(aapl.asfreq("M", method="bfill"))

# Add a column `diff` to `aapl` 
aapl['diff'] = aapl.Open - aapl.Close
aapl['diff'] = aapl['Open'] - aapl['Close']

# Delete the new `diff` column
# del aapl['diff']

aapl.Close.plot(grid = True)
## plt.show() 

# Ajust daily close
daily_close = aapl['Adj Close'] 

# Calculate returns
daily_pct_change = daily_close.pct_change()
daily_pct_change.fillna(0, inplace = True)

# Daily log returns
daily_log_returns = np.log(daily_close.pct_change()+1)

print(daily_pct_change.loc['2011'].tail())
print(daily_log_returns.loc['2011'].tail())
