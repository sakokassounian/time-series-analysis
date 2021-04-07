#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 10:40:36 2021

@author: sarkis
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

ann_f = 365 # daily

#bank money
data = pd.read_csv("expenses.csv")
data.rename(columns={'P&L': 'trans'},inplace=True)
data.date=pd.to_datetime(data.date)
data.sort_values(by=['date'],inplace=True)
data_daily = data.groupby("date").agg({'trans':'sum'})
date_r = pd.date_range(start=data_daily.index[0],end=data_daily.index[-1],freq='D')
data_extend = data_daily.reindex(date_r,fill_value=0)

#outer money    
current =  5300
max_budge = 7200
external = max_budge - current  
external = external / (len(data_extend) - 1)
external = len(data_extend)*[-external ]

#total money
data_extend['external'] = external
data_extend['tot'] = data_extend.trans + data_extend.external


#analysis
data_extend['cum'] = data_extend.tot.cumsum()
data_extend['nominal'] = data_extend.cum + max_budge 
data_extend['returns'] = [np.nan]+ [-1+(data_extend.nominal.iloc[i]/data_extend.nominal.iloc[i-1])  for i in range(1,len(data_extend))]


AAR = (ann_f*0.5)*np.nanmean(data_extend.returns)
std = (ann_f**0.5)*np.nanstd(data_extend.returns,ddof=1)
IR = AAR /std 
#%%

data_extend['nominal'].plot(figsize=(12,12))
plt.suptitle(f'IR = {IR}',fontsize=25)
plt.show()

