#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 12:15:41 2020

@author: Andrew
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import mca
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from sklearn.metrics import f1_score
from scipy.cluster.hierarchy import linkage, fcluster
#from scipy.cluster.vq import kmeans,vq

data_cluster = pd.read_csv('Covid-19.csv')

#establish readable format of time series
startdate = pd.to_datetime(data_cluster['starttime']).dt.date
data_cluster['time'] = startdate

#reapplying names
data_cluster['trump'] = data_cluster['dfp_public_figure_ap_1']
data_cluster['mnuchin'] = data_cluster['dfp_public_figure_ap_2']
data_cluster['pelosi'] = data_cluster['dfp_public_figure_ap_3']
data_cluster['mcconnell'] = data_cluster['dfp_public_figure_ap_4']
data_cluster['shumer'] = data_cluster['dfp_public_figure_ap_5']
data_cluster['cuomo'] = data_cluster['dfp_public_figure_ap_6']
data_cluster['newsom'] = data_cluster['dfp_public_figure_ap_7']
data_cluster['biden'] = data_cluster['dfp_public_figure_ap_8']
data_cluster['pence'] = data_cluster['dfp_public_figure_ap_9']
data_cluster['cdc'] = data_cluster['dfp_public_figure_ap_10']

dict = {'trump':data_cluster['trump'], 
        'mnuchin':data_cluster['mnuchin'], 
        'pelosi':data_cluster['pelosi'],
        'mcconnell':data_cluster['mcconnell'], 
        'cuomo':data_cluster['cuomo'], 
        'newsom':data_cluster['newsom'],
        'biden':data_cluster['biden'], 
        'pence':data_cluster['pence'],
        'cdc':data_cluster['cdc']}

#define dict for the mca
X = pd.DataFrame(dict)

X_trump = pd.get_dummies(X['trump'].astype(str), prefix='trump')
X_mnuchin = pd.get_dummies(X['mnuchin'].astype(str), prefix='mnuchin')
X_pelosi = pd.get_dummies(X['pelosi'].astype(str), prefix='pelosi')
X_mcconnell = pd.get_dummies(X['mcconnell'].astype(str), prefix='mcconnell')
X_cuomo = pd.get_dummies(X['cuomo'].astype(str), prefix='cuomo')
X_newson = pd.get_dummies(X['newsom'].astype(str), prefix='newsom')
X_biden = pd.get_dummies(X['biden'].astype(str), prefix='biden')
X_pence = pd.get_dummies(X['pence'].astype(str), prefix='pence')
X_cdc = pd.get_dummies(X['cdc'].astype(str), prefix='cdc')

X = pd.concat([X_trump, X_mnuchin, 
               X_pelosi, X_mcconnell, 
               X_cuomo, X_newson, 
               X_biden, X_pence, X_cdc], axis = 1, sort=False)

ncols = len(X.columns)
mca_X = mca.MCA(X, ncols = ncols)

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

#transform array to df, name the labels, d/r as hue
mca_2 = mca_X.fs_r(N=2)
df_mca_2 = pd.DataFrame(mca_2,columns=['dim_A','dim_B'])
df_mca_2['ideo']=data_cluster['ideo5']

cleanup_ideo = {"idéologie": {"Very conservative": 'Conservative', 
                         "Very liberal": 'Liberal'}}
df_mca_2.replace(cleanup_ideo, inplace=True)



plt.figure()
sns.scatterplot(x='dim_A', y='dim_B', hue='ideo', data = df_mca_2)

#3-dimension figure
mca_3 = mca_X.fs_r(N=3)
df_mca_3 = pd.DataFrame(mca_3,columns=['dim_A','dim_B', 'dim_C'])
df_mca_3['ideo']=data_cluster['ideo5']
df_mca_3['ideo_alt'] = df_mca_3['ideo']
df_mca_3['ideo_alt'][(df_mca_3['ideo'].astype(str) == 'Very conservative') | (df_mca_3['ideo'].astype(str) == 'Conservative')] = 'conservative' 
df_mca_3['ideo_alt'][(df_mca_3['ideo'].astype(str) == 'Very liberal') | (df_mca_3['ideo'].astype(str) == 'Liberal')] = 'liberal' 
df_mca_3['ideo_alt'][df_mca_3['ideo'].astype(str) == 'moderate'] = 'moderate' 

plt.figure()
x = np.asarray(df_mca_3[df_mca_3['ideo_alt'] == 'liberal']['dim_A'])
y = np.asarray(df_mca_3[df_mca_3['ideo_alt'] == 'liberal']['dim_B'])
z = np.asarray(df_mca_3[df_mca_3['ideo_alt'] == 'liberal']['dim_C'])
fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(x, y, z, marker = 'o', color = 'r', alpha = 0.5)
x = np.asarray(df_mca_3[df_mca_3['ideo_alt'] == 'conservative']['dim_A'])
y = np.asarray(df_mca_3[df_mca_3['ideo_alt'] == 'conservative']['dim_B'])
z = np.asarray(df_mca_3[df_mca_3['ideo_alt'] == 'conservative']['dim_C'])
ax.scatter(x, y, z, marker = 'o', color = 'b', alpha = 0.5)