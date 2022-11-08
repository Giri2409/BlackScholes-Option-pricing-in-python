# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 15:36:07 2022
@author: Giri
"""
!pip install pandas_datareader
!pip install matplotlib
!pip install python-math

from math import log, sqrt, pi, exp
from scipy.stats import norm

from datetime import datetime, date
import numpy as np
import pandas as pd
import pandas_datareader.data as web

import matplotlib.pyplot as plt

#d1 calculation
def d1(S,K,T,r,sigma):
    return(log(S/K)+(r+sigma**2/2.)*T)/(sigma*sqrt(T))
#d2 calculation
def d2(S,K,T,r,sigma):
    return d1(S,K,T,r,sigma)-sigma*sqrt(T)
#BS_call
def bs_call(S,K,T,r,sigma):
    return S*norm.cdf(d1(S,K,T,r,sigma))-K*exp(-r*T)*norm.cdf(d2(S,K,T,r,sigma))
 #BS_put 
def bs_put(S,K,T,r,sigma):
    return K*exp(-r*T)-S*bs_call(S,K,T,r,sigma)

s ='TSLA'
T ='11-25-2022'
k = 205

today = datetime.now()
one_year_ago= today.replace(year=today.year-1)

df=web.DataReader(s,'yahoo',one_year_ago,today)

#price movement graph
close = df['Close']
ax=close.plot(title='TESLA')
ax.set_xlabel('Date')
ax.set_ylabel('Close')
ax.grid()
plt.show()

##sigma calculation
df=df.sort_values(by='Date')
df=df.dropna()
df = df.assign(close_day_before=df.Close.shift(1))
df['returns'] = ((df.Close - df.close_day_before)/df.close_day_before)

sigma = np.sqrt(252) * df['returns'].std()

#Treasury Yield 10 Years (^TNX)  - riskfree rate of return
#iloc function helps to select a specific row or column from dataset

r = (web.DataReader(
    "^TNX", 'yahoo', today.replace(day=today.day-1), today)['Close'].iloc[-1])/100

spot = df['Close'].iloc[-1]
#strptime for date format

t = (datetime.strptime(T, "%m-%d-%Y") - datetime.utcnow()).days / 365

print('The Option Price is: ', bs_call(spot, k, t, r, sigma))




