# -*- coding: utf-8 -*-
"""
Created on Tue May 26 16:50:56 2020

@author: guosj
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
#from sklearn.model_selection import RandomizedSearchCV

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
        'employ':data['employ'], 'time':data['time'], 'pres':pres_2020}
X = pd.DataFrame(dict) 

X = X.loc[(X.pres == "Donald Trump (Republican)") | (X.pres == "Joe Biden (Democrat)")]


X_gender = pd.get_dummies(X['gender'], prefix='gender')
X_ideo = pd.get_dummies(X['ideo'], prefix='ideo')
X_news = pd.get_dummies(X['news'].astype(str), prefix='news')
X_corona = pd.get_dummies(X['corona'].astype(str), prefix='corona')
X_stimulus = pd.get_dummies(X['stimulus'].astype(str), prefix='stimulus')
X_employ = pd.get_dummies(X['employ'].astype(str), prefix='employ')
X_time = pd.get_dummies(X['time'].astype(str), prefix='time')
X_pres = pd.get_dummies(X['pres'].astype(str), prefix='pres')
y = X_pres['pres_Donald Trump (Republican)']

X = pd.concat([X_gender, X_ideo, X_news, X_corona, X_stimulus, X_employ, X_time], axis = 1, sort=False)

'''
time_unique = X.time.unique()
X_6 = X.loc[X.time == time_unique[0]] #data of wave 6
X_5 = X.loc[X.time == time_unique[1]]
X_4 = X.loc[X.time == time_unique[2]]
X_3 = X.loc[X.time == time_unique[3]]
X_2 = X.loc[X.time == time_unique[4]]
X_1 = X.loc[X.time == time_unique[5]]


y_6 = pres_2020[X.time == time_unique[0]]
y_5 = pres_2020[X.time == time_unique[1]]
y_4 = pres_2020[X.time == time_unique[2]]
y_3 = pres_2020[X.time == time_unique[3]]
y_2 = pres_2020[X.time == time_unique[4]]
y_1 = pres_2020[X.time == time_unique[5]]
'''

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, stratify = data.iloc[X.index,:]['time'], random_state = 0)

n_estimators = [int(x) for x in np.linspace(start = 50, stop = 500, num = 10)]
max_features = [float(x) for x in np.linspace(start = 0.4, stop = 0.9, num = 10)]
max_depth = [int(x) for x in np.linspace(5, 100, num = 20)]
max_depth.append(None)

random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth}

#clf = RandomForestClassifier()

#clf_random = RandomizedSearchCV(estimator=clf, param_distributions=random_grid, n_iter=200, cv=5, n_jobs=-1, verbose=2, random_state = 1)

#X_6_train, X_6_test, y_6_train, y_6_test = train_test_split(X_6, y_6, test_size = 0.3)
clf = RandomForestClassifier(n_estimators = 300, max_depth = 5, max_features = 0.7888888888888889, random_state = 1)
#clf_random.fit(X_train, y_train)
#print(clf_random.best_params_)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
print("Training accuracy of the random forest classifier is: ", metrics.accuracy_score(y_train, clf.predict(X_train)))
print("Testing accuracy of the random forest classifier is: ", metrics.accuracy_score(y_test, y_pred))

feats = {}

for feature, importance in zip(X.columns, clf.feature_importances_):
    feats[feature] = importance
    
importances = pd.DataFrame.from_dict(feats, orient='index').rename(columns={0: 'Gini-importance'})
importances = importances.sort_values(by='Gini-importance', ascending=False)
importances_top = importances.iloc[0:10,]


dict = {'x':importances_top.iloc[:,0].values.T, 'y': importances_top.index}
df = pd.DataFrame(dict)
sns.set()
sns.barplot(x='x', y='y', data=df, color='skyblue')
plt.title('Feature importance in RandomForest Classifier')
plt.xlabel('Relative importance')
plt.ylabel('feature') 
plt.show()
