#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 23:20:17 2020

@author: sguo
"""
from sklearn.feature_extraction.text import TfidfVectorizer
import seaborn as sns
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt

data = pd.read_csv('cuomo.csv')

time = pd.to_datetime(data['date'])
data['date'] = time.dt.date
startweek = datetime.date(2020, 4, 12)
endweek = datetime.date(2020, 5, 23)
data_tv = data[(data['date'] >= startweek) & (data['date'] <= endweek)]

tv = TfidfVectorizer(stop_words = 'english', max_features = 5000,
                     token_pattern=u'(?ui)\\b\\w*[a-z]+\\w*\\b', use_idf = False)

tv_transformed = tv.fit_transform(data_tv['body'].astype(str))
tv_df = pd.DataFrame(tv_transformed.toarray(), columns=tv.get_feature_names())

#frequency of keywords
coronavirus = tv_df.coronavirus
corona = tv_df.corona
covid = tv_df.covid
pandemic = tv_df.pandemic
corona_final = coronavirus + corona + pandemic + covid
reopen = tv_df.reopen
reopening = tv_df.reopening
reopened = tv_df.reopened
open = tv_df.open
opening = tv_df.opening
reopen_final = reopen + reopening + reopened + open + opening
trump = tv_df.trump
source = data['source'][(data['date'] >= startweek) & (data['date'] <= endweek)]

dict = {'date':data_tv['date'], 'corona':corona_final, 'reopen':reopen_final, 'source':source, 
        'open':open, 'trump':trump}

#group by news source and week
df=pd.DataFrame(dict)
df['date'] = pd.to_datetime(df['date'])
df_corona_source = df.groupby(['source', pd.Grouper(key='date', freq='W-TUE')])['corona'].mean().reset_index().sort_values('date')
df_corona_source.drop(df_corona_source.tail(4).index, inplace=True)
df_reopen_source = df.groupby(['source', pd.Grouper(key='date', freq='W-TUE')])['reopen'].mean().reset_index().sort_values('date')
df_reopen_source.drop(df_reopen_source.tail(4).index, inplace=True)
df_trump_source = df.groupby(['source', pd.Grouper(key='date', freq='W-TUE')])['trump'].mean().reset_index().sort_values('date')

#group just by week
df_corona = df.resample('W-TUE', on='date')['corona'].mean().reset_index().sort_values('date')
df_corona.drop(6, inplace=True)
df_reopen = df.resample('W-TUE', on='date')['reopen'].mean().reset_index().sort_values('date')
df_reopen.drop(6, inplace=True)

month_day=df_corona_source['date'].dt.strftime('%m%d')

sns.set
plt.figure()
fig = sns.lineplot(x=month_day, y='corona', data=df_corona)

plt.figure()
fig = sns.lineplot(x=month_day, y='reopen', data=df_reopen)

plt.figure()
fig = sns.lineplot(x=month_day, y='corona', hue='source', data=df_corona_source)
plt.title('corona')

plt.figure()
fig = sns.lineplot(x=month_day, y='reopen', hue='source', data=df_reopen_source)
plt.title('reopen')