#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 21:42:43 2020

@author: sguo
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import RandomizedSearchCV

data = pd.read_csv('covid.csv')

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
        'employ':data['employ'], 'time':data['time'], 'pres':pres_2020, 'race':data['race4'],
        'deficit':data['deficit'], 'econ':data['dfp_nav_opinion']}
X = pd.DataFrame(dict) 

X = X.loc[(X.pres == "Donald Trump (Republican)") | (X.pres == "Joe Biden (Democrat)")]


X_gender = pd.get_dummies(X['gender'].astype(str), prefix='gender')
X_ideo = pd.get_dummies(X['ideo'].astype(str), prefix='ideo')
X_news = pd.get_dummies(X['news'].astype(str), prefix='news')
X_corona = pd.get_dummies(X['corona'].astype(str), prefix='corona')
X_stimulus = pd.get_dummies(X['stimulus'].astype(str), prefix='stimulus')
X_employ = pd.get_dummies(X['employ'].astype(str), prefix='employ')
X_time = pd.get_dummies(X['time'].astype(str), prefix='time')
X_pres = pd.get_dummies(X['pres'].astype(str), prefix='pres')
X_race = pd.get_dummies(X['race'].astype(str), prefix='race')
X_deficit = pd.get_dummies(X['deficit'].astype(str), prefix='deficit').iloc[:,0]
X_deficit.name = 'deficit_The government has spent enough'
X_econ = pd.get_dummies(X['econ'].astype(str), prefix='econ')

X = pd.concat([X_gender, X_ideo, X_news, X_corona, X_stimulus, X_employ, X_time, X_race, X_deficit, X_econ], axis = 1, sort=False)
X.dropna(inplace=True)

y_trump = data['dfp_public_figure_ap_1'].iloc[X.index]
y_trump = y_trump.str.replace('Strongly approve', 'approve')
y_trump = y_trump.str.replace('Somewhat approve', 'approve')
y_trump = y_trump.str.replace('Strongly disapprove', 'disapprove')
y_trump = y_trump.str.replace('Somewhat disapprove', 'disapprove')
y_trump = y_trump.loc[y_trump.values != 'Not sure']
y_trump.dropna(inplace=True)

X_trump = X.loc[y_trump.index,:]

y_newsom = data['dfp_public_figure_ap_7'].iloc[X.index]
y_newsom = y_newsom.str.replace('Strongly approve', 'approve')
y_newsom = y_newsom.str.replace('Somewhat approve', 'approve')
y_newsom = y_newsom.str.replace('Strongly disapprove', 'disapprove')
y_newsom = y_newsom.str.replace('Somewhat disapprove', 'disapprove')
y_newsom= y_newsom.loc[y_newsom.values != 'Not sure']
y_newsom.dropna(inplace=True)

X_newsom = X.loc[y_newsom.index,:]

y_cuomo = data['dfp_public_figure_ap_6'].iloc[X.index]
y_cuomo = y_cuomo.str.replace('Strongly approve', 'approve')
y_cuomo = y_cuomo.str.replace('Somewhat approve', 'approve')
y_cuomo = y_cuomo.str.replace('Strongly disapprove', 'disapprove')
y_cuomo = y_cuomo.str.replace('Somewhat disapprove', 'disapprove')
y_cuomo = y_cuomo.loc[y_cuomo.values != 'Not sure']
y_cuomo.dropna(inplace=True)

X_cuomo = X.loc[y_cuomo.index,:]

X_trump_train, X_trump_test, y_trump_train, y_trump_test = train_test_split(X_trump, y_trump, test_size = 0.3, stratify = data.iloc[X_trump.index,:]['time'], random_state = 42)
X_newsom_train, X_newsom_test, y_newsom_train, y_newsom_test = train_test_split(X_newsom, y_newsom, test_size = 0.3, stratify = data.iloc[X_newsom.index,:]['time'], random_state = 42)
X_cuomo_train, X_cuomo_test, y_cuomo_train, y_cuomo_test = train_test_split(X_cuomo, y_cuomo, test_size = 0.3, stratify = data.iloc[X_cuomo.index,:]['time'], random_state = 42)

'''
n_estimators = [int(x) for x in np.linspace(start = 50, stop = 500, num = 10)]
max_features = [float(x) for x in np.linspace(start = 0.4, stop = 1, num = 13)]
max_depth = [int(x) for x in np.linspace(1, 20, num = 20)]
max_depth.append(None)


random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth}

clf = RandomForestClassifier()
clf_random = RandomizedSearchCV(estimator=clf, param_distributions=random_grid, n_iter=200, cv=5, n_jobs=-1, verbose=2, random_state = 42)
clf_random.fit(X_cuomo_train, y_cuomo_train)
print(clf_random.best_params_)


'''

clf_trump = RandomForestClassifier(n_estimators=300, max_features=0.4, max_depth=7)
clf_trump.fit(X_trump_train, y_trump_train)
y_trump_pred = clf_trump.predict(X_trump_test)
print("Training accuracy of the random forest classifier for Trump is: ", metrics.accuracy_score(y_trump_train, clf_trump.predict(X_trump_train)))
print("Testing accuracy of the random forest classifier for Trump is: ", metrics.accuracy_score(y_trump_test, y_trump_pred))

feats = {}

for feature, importance in zip(X_trump.columns, clf_trump.feature_importances_):
    feats[feature] = importance
    
importances = pd.DataFrame.from_dict(feats, orient='index').rename(columns={0: 'Gini-importance'})
importances = importances.sort_values(by='Gini-importance', ascending=False)
importances_top = importances.iloc[0:10,]


dict = {'x':importances_top.iloc[:,0].values.T, 'y': importances_top.index}
df = pd.DataFrame(dict)
sns.set()
plt.figure()
sns.barplot(x='x', y='y', data=df, color='skyblue')
plt.title('Features importance in RandomForest Classifier for Trump')
plt.xlabel('Relative importance')
plt.ylabel('feature') 
plt.show()

clf_newsom = RandomForestClassifier(n_estimators=50, max_features=0.7, max_depth=7)
clf_newsom.fit(X_newsom_train, y_newsom_train)
y_newsom_pred = clf_newsom.predict(X_newsom_test)
print("Training accuracy of the random forest classifier for Newsom is: ", metrics.accuracy_score(y_newsom_train, clf_newsom.predict(X_newsom_train)))
print("Testing accuracy of the random forest classifier for Newsom is: ", metrics.accuracy_score(y_newsom_test, y_newsom_pred))

feats = {}

for feature, importance in zip(X_newsom.columns, clf_newsom.feature_importances_):
    feats[feature] = importance
    
importances = pd.DataFrame.from_dict(feats, orient='index').rename(columns={0: 'Gini-importance'})
importances = importances.sort_values(by='Gini-importance', ascending=False)
importances_top = importances.iloc[0:10,]


dict = {'x':importances_top.iloc[:,0].values.T, 'y': importances_top.index}
df = pd.DataFrame(dict)
sns.set()
plt.figure()
sns.barplot(x='x', y='y', data=df, color='skyblue')
plt.title('Features importance in RandomForest Classifier for Newsom approval')
plt.xlabel('Relative importance')
plt.ylabel('feature') 
plt.show()

clf_cuomo = RandomForestClassifier(n_estimators=150, max_features=0.55, max_depth=7)
clf_cuomo.fit(X_cuomo_train, y_cuomo_train)
y_cuomo_pred = clf_cuomo.predict(X_cuomo_test)
print("Training accuracy of the random forest classifier for Cuomo is: ", metrics.accuracy_score(y_cuomo_train, clf_cuomo.predict(X_cuomo_train)))
print("Testing accuracy of the random forest classifier for Cuomo is: ", metrics.accuracy_score(y_cuomo_test, y_cuomo_pred))

feats = {}

for feature, importance in zip(X_cuomo.columns, clf_cuomo.feature_importances_):
    feats[feature] = importance
    
importances = pd.DataFrame.from_dict(feats, orient='index').rename(columns={0: 'Gini-importance'})
importances = importances.sort_values(by='Gini-importance', ascending=False)
importances_top = importances.iloc[0:10,]


dict = {'x':importances_top.iloc[:,0].values.T, 'y': importances_top.index}
df = pd.DataFrame(dict)
sns.set()
plt.figure()
sns.barplot(x='x', y='y', data=df, color='skyblue')
plt.title('Features importance in RandomForest Classifier for Cuomo Approval')
plt.xlabel('Relative importance')
plt.ylabel('feature') 
plt.show()