# -*- coding: utf-8 -*-
"""
Created on Mon May 25 21:28:17 2020

@author: guosj
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mca
import seaborn as sns
#from sklearn.preprocessing import LabelEncoder, OneHotEncoder

data = pd.read_csv('MCA_Data.csv')

startdate = pd.to_datetime(data['starttime']).dt.date
data['time'] = startdate

pres_2020 = [];
for i in range(0, data.shape[0]):
    if(data['pres_2020'][i] == 'Not sure'):
        pres_2020.append(data['pres_2020lean'][i])
    else:
        pres_2020.append(data['pres_2020'][i])
        
dict = {'gender':data['gender'], 'education':data['education'], 'ideo':data['ideo5'],
        'news':data['newsint'], 'corona':data['corona1'], 'stimulus':data['stimulus_check'],
        'employ':data['employ'], 'time':data['time']}
X = pd.DataFrame(dict)

X_gender = pd.get_dummies(X['gender'], prefix='gender')
X_ideo = pd.get_dummies(X['ideo'], prefix='ideo')
X_news = pd.get_dummies(X['news'].astype(str), prefix='news')
X_corona = pd.get_dummies(X['corona'].astype(str), prefix='corona')
X_stimulus = pd.get_dummies(X['stimulus'].astype(str), prefix='stimulus')
X_employ = pd.get_dummies(X['employ'].astype(str), prefix='employ')
X_time = pd.get_dummies(X['time'].astype(str), prefix='time')

X = pd.concat([X_gender, X_ideo, X_news, X_corona, X_stimulus, X_employ, X_time], axis = 1, sort=False)

ncols = len(X.columns)
mca_X = mca.MCA(X, ncols = ncols)
#print(mca_X.fs_r(1))
print(mca_X.L)
print(sum(mca_X.L))

N_eig_all = np.linspace(1,100,100, dtype=int)

Expl_var_bn = []
Expl_var_bnga = []
for N_eig in N_eig_all:
    Expl_var_bn.append(np.sum(mca_X.expl_var(greenacre=False,
                                               N=N_eig)))
    Expl_var_bnga.append(np.sum(mca_X.expl_var(greenacre=True, 
                                      N=N_eig)))

sns.set()
plt.figure(figsize=(8,5))
plt.plot(N_eig_all,Expl_var_bn, label='Benzecri correction')
plt.plot(N_eig_all,Expl_var_bnga,label='Benzecri & Greenacre correction')
plt.legend(loc='lower right')
plt.ylim(0,1.1)
plt.xlim(1,40)


'''
le = LabelEncoder()

X['gender'] = le.fit_transform(X['gender'])
X['ideo'] = le.fit_transform(X['ideo'])
X['news'] = le.fit_transform(X['news'].astype(str))
X['corona'] = le.fit_transform(X['corona'].astype(str))
X['stimulus'] = le.fit_transform(X['stimulus'].astype(str))
X['employ'] = le.fit_transform(X['employ'].astype(str))

ohe = OneHotEncoder(sparse=False)
X = ohe.fit_transform(X)
'''

