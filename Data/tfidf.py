# -*- coding: utf-8 -*-
"""
Created on Thu May 28 21:46:07 2020

@author: guosj
"""

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
import datetime

data = pd.read_csv('news.csv')

time = pd.to_datetime(data['timestamp'])
data['date'] = time.dt.date
startweek = datetime.date(2020, 4, 14)
endweek = datetime.date(2020, 5, 19)
data_tv = data[(data['date'] >= startweek) & (data['date'] <= endweek)]

tv = TfidfVectorizer(stop_words = 'english', max_features = 1000, max_df = 0.5,
                     token_pattern=u'(?ui)\\b\\w*[a-z]+\\w*\\b', use_idf = False)

tv_transformed = tv.fit_transform(data_tv['description'].astype(str))
tv_df = pd.DataFrame(tv_transformed.toarray(), columns=tv.get_feature_names())

corona = tv_df.coronavirus
reopen = tv_df.reopen
open = tv_df.open
trump = tv_df.trump
source = data['source'][(data['date'] >= startweek) & (data['date'] <= endweek)]

dict = {'date':data_tv['date'], 'corona':corona, 'reopen':reopen, 'source':source, 
        'open':open, 'trump':trump}

df=pd.DataFrame(dict)
df['date'] = pd.to_datetime(df['date']) 
df_corona = df.groupby(['source', pd.Grouper(key='date', freq='W-TUE')])['corona'].mean().reset_index().sort_values('date')
df_reopen = df.groupby(['source', pd.Grouper(key='date', freq='W-TUE')])['reopen'].mean().reset_index().sort_values('date')
df_open = df.groupby(['source', pd.Grouper(key='date', freq='W-TUE')])['open'].mean().reset_index().sort_values('date')
df_trump = df.groupby(['source', pd.Grouper(key='date', freq='W-TUE')])['trump'].mean().reset_index().sort_values('date')