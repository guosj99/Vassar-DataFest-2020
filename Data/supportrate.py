#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 19:16:23 2020

@author: sguo
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


data = pd.read_csv('data_final.csv')

startdate = pd.to_datetime(data['starttime']).dt.date
data['time'] = startdate
pres_2020 = [];

for i in range(0, data.shape[0]):
    if(data['pres_2020'][i] == 'Not sure'):
        pres_2020.append(data['pres_2020lean'][i])
    else:
        pres_2020.append(data['pres_2020'][i])

data['pres_2020_new'] = pres_2020

df = data.groupby('time')['pres_2020_new'].value_counts()
df_pcts = df.groupby(level = 0).apply(lambda x: 100 * x / float(x.sum()))
'''
plt1 = df_pcts.unstack(0).plot.bar()
plt2 = df_pcts.unstack().plot.bar()
plt2.legend(loc='center left',bbox_to_anchor=(1.0, 0.5))
'''

data['Donald Trump'] = data['dfp_public_figure_ap_1']
data['Steven Mnuchin'] = data['dfp_public_figure_ap_2']
data['Nancy Pelosi'] = data['dfp_public_figure_ap_3']
data['Mitch McConnell'] = data['dfp_public_figure_ap_4']
data['Chuck Shumer'] = data['dfp_public_figure_ap_5']
data['Andrew Cuomo'] = data['dfp_public_figure_ap_6']
data['Gavin Newsom'] = data['dfp_public_figure_ap_7']
data['Joe Biden'] = data['dfp_public_figure_ap_8']
data['Mike Pence'] = data['dfp_public_figure_ap_9']
data['CDC'] = data['dfp_public_figure_ap_10']

dfp_1 = data.groupby('time')['Donald Trump'].value_counts().groupby(level=0).apply(lambda x: 100 * x / float(x.sum()))
#dfp_plot_1 = dfp_1.unstack(0).plot.bar()

dfp_2 = data.groupby('time')['Steven Mnuchin'].value_counts().groupby(level=0).apply(lambda x: 100 * x / float(x.sum()))
#dfp_plot_2 = dfp_2.unstack(0).plot.bar()

dfp_3 = data.groupby('time')['Nancy Pelosi'].value_counts().groupby(level=0).apply(lambda x: 100 * x / float(x.sum()))
#dfp_plot_3 = dfp_3.unstack(0).plot.bar()

dfp_4 = data.groupby('time')['Mitch McConnell'].value_counts().groupby(level=0).apply(lambda x: 100 * x / float(x.sum()))
#dfp_plot_4 = dfp_4.unstack(0).plot.bar()

dfp_5 = data.groupby('time')['Chuck Shumer'].value_counts().groupby(level=0).apply(lambda x: 100 * x / float(x.sum()))
#dfp_plot_5 = dfp_5.unstack(0).plot.bar()

dfp_6 = data.groupby('time')['Andrew Cuomo'].value_counts().groupby(level=0).apply(lambda x: 100 * x / float(x.sum()))
#dfp_plot_6 = dfp_6.unstack(0).plot.bar()

dfp_7 = data.groupby('time')['Gavin Newsom'].value_counts().groupby(level=0).apply(lambda x: 100 * x / float(x.sum()))
#dfp_plot_7 = dfp_7.unstack(0).plot.bar()

dfp_8 = data.groupby('time')['Joe Biden'].value_counts().groupby(level=0).apply(lambda x: 100 * x / float(x.sum()))
#dfp_plot_8 = dfp_8.unstack(0).plot.bar()

dfp_9 = data.groupby('time')['Mike Pence'].value_counts().groupby(level=0).apply(lambda x: 100 * x / float(x.sum()))
#dfp_plot_9 = dfp_9.unstack(0).plot.bar()

dfp_10 = data.groupby('time')['CDC'].value_counts().groupby(level=0).apply(lambda x: 100 * x / float(x.sum()))
#dfp_plot_10 = dfp_10.unstack(0).plot.bar()

dict = {'Donald Trump' : data['Donald Trump'].value_counts().apply(lambda x: 100 * x / data['Donald Trump'].value_counts().sum()), 
        'Steven Mnuchin' : data['Steven Mnuchin'].value_counts().apply(lambda x: 100 * x / data['Steven Mnuchin'].value_counts().sum()),
        'Nancy Peolosi' : data['Nancy Pelosi'].value_counts().apply(lambda x: 100 * x / data['Nancy Pelosi'].value_counts().sum()),
        'Mitch McConnell' : data['Mitch McConnell'].value_counts().apply(lambda x: 100 * x / data['Mitch McConnell'].value_counts().sum()),
        'Chuck Shumer' : data['Chuck Shumer'].value_counts().apply(lambda x: 100 * x / data['Chuck Shumer'].value_counts().sum()), 
        'Andrew Cuomo' : data['Andrew Cuomo'].value_counts().apply(lambda x: 100 * x / data['Andrew Cuomo'].value_counts().sum()),
        'Gavin Newsom' : data['Gavin Newsom'].value_counts().apply(lambda x: 100 * x / data['Gavin Newsom'].value_counts().sum()),
        'Joe Biden' : data['Joe Biden'].value_counts().apply(lambda x: 100 * x / data['Joe Biden'].value_counts().sum()),
        'Mike Pence' : data['Mike Pence'].value_counts().apply(lambda x: 100 * x / data['Mike Pence'].value_counts().sum()),
        'CDC' : data['CDC'].value_counts().apply(lambda x: 100 * x / data['CDC'].value_counts().sum())}
approval_data = pd.DataFrame(dict, index=data['Donald Trump'].value_counts().keys())

approve = approval_data.loc['Strongly approve',:] + approval_data.loc['Somewhat approve',:]
disapprove = approval_data.loc['Strongly disapprove',:] + approval_data.loc['Somewhat disapprove',:]

df = pd.DataFrame()
final_approval = pd.concat((df, approve.rename('approve')), axis=1)
final_approval = pd.concat((final_approval, disapprove.rename('disapprove')), axis=1)

trump = data['Donald Trump']
trump.index = data['time']
newsom = data['Gavin Newsom']
newsom.index = data['time']
cuomo = data['Andrew Cuomo']
cuomo.index = data['time']

trump = trump.str.replace('Strongly approve', 'approve')
trump = trump.str.replace('Somewhat approve', 'approve')
trump = trump.str.replace('Strongly disapprove', 'disapprove')
trump = trump.str.replace('Somewhat disapprove', 'disapprove')

newsom = newsom.str.replace('Strongly approve', 'approve')
newsom = newsom.str.replace('Somewhat approve', 'approve')
newsom = newsom.str.replace('Strongly disapprove', 'disapprove')
newsom = newsom.str.replace('Somewhat disapprove', 'disapprove')

cuomo = cuomo.str.replace('Strongly approve', 'approve')
cuomo = cuomo.str.replace('Somewhat approve', 'approve')
cuomo = cuomo.str.replace('Strongly disapprove', 'disapprove')
cuomo = cuomo.str.replace('Somewhat disapprove', 'disapprove')

trump_group = trump.groupby('time').value_counts()
newsom_group = newsom.groupby('time').value_counts()
cuomo_group = cuomo.groupby('time').value_counts()

x = []
trump_approve = []
newsom_approve = []
cuomo_approve = []
trump_disapprove = []
newsom_disapprove = []
cuomo_disapprove = []
trump_notsure = []
newsom_notsure = []
cuomo_notsure = []

for date, app in trump_group.index:
    x.append(date)
    if(app == 'approve'):
        trump_approve.append(trump_group.loc[date, app])
        newsom_approve.append(newsom_group.loc[date,app])
        cuomo_approve.append(cuomo_group.loc[date,app])
    elif(app == 'disapprove'):
        trump_disapprove.append(trump_group.loc[date, app])
        newsom_disapprove.append(newsom_group.loc[date,app])
        cuomo_disapprove.append(cuomo_group.loc[date,app])
    else:
        trump_notsure.append(trump_group.loc[date, app])
        newsom_notsure.append(newsom_group.loc[date,app])
        cuomo_notsure.append(cuomo_group.loc[date,app])

lists_trump = [trump_approve, trump_disapprove, trump_notsure]
lists_newsom = [newsom_approve, newsom_disapprove, newsom_notsure]
lists_cuomo = [cuomo_approve, cuomo_disapprove, cuomo_notsure]

trump_sum = [sum(x) for x in zip(*lists_trump)]
newsom_sum = [sum(x) for x in zip(*lists_newsom)]
cuomo_sum = [sum(x) for x in zip(*lists_cuomo)]

x = set(x)
x = list(x)
format_date = []
for date in x:
    format_date.append(date.strftime('%m%d'))

for i in range(0, len(x)):        
    trump_approve[i] = trump_approve[i] / trump_sum[i]
    trump_disapprove[i] = trump_disapprove[i] / trump_sum[i]
    newsom_approve[i] = newsom_approve[i] / newsom_sum[i]
    newsom_disapprove[i] = newsom_disapprove[i] / newsom_sum[i]
    cuomo_approve[i] = cuomo_approve[i] / cuomo_sum[i]
    cuomo_disapprove[i] = cuomo_disapprove[i] / cuomo_sum[i]
    
sns.set()
plt.figure()
sns.lineplot(x=format_date, y=trump_approve)
sns.lineplot(x=format_date, y=trump_disapprove)
labels=['approve','disapprove']
plt.legend(labels)
plt.xlabel('Date')
plt.ylabel('Rate')
plt.title('Trump Aprroval Rate')

plt.figure()
sns.lineplot(x=format_date, y=newsom_approve)
sns.lineplot(x=format_date, y=newsom_disapprove)
labels=['approve','disapprove']
plt.legend(labels)
plt.xlabel('Date')
plt.ylabel('Rate')
plt.title('Newsom Aprroval Rate')

plt.figure()
sns.lineplot(x=format_date, y=cuomo_approve)
sns.lineplot(x=format_date, y=cuomo_disapprove)
labels=['approve','disapprove']
plt.legend(labels)
plt.xlabel('Date')
plt.ylabel('Rate')
plt.title('Cuomo Aprroval Rate')
      