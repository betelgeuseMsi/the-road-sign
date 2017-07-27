import pandas as pd

train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")

train.head(2)

train['DetectedCamera'].value_counts()

#encode as integer
mapping = {'Front':0, 'Right':1, 'Left':2, 'Rear':3}
train = train.replace({'DetectedCamera':mapping})
test = test.replace({'DetectedCamera':mapping})

#renaming column
train.rename(columns = {'SignFacing (Target)': 'Target'}, inplace=True)

#encode Target Variable based on sample submission file
mapping = {'Front':0, 'Left':1, 'Rear':2, 'Right':3}
train = train.replace({'Target':mapping})

#target variable
y_train = train['Target']
test_id = test['Id']

#drop columns
train.drop(['Target','Id'], inplace=True, axis=1)
test.drop('Id',inplace=True,axis=1)

#train model
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(n_estimators=500,max_features=3,min_samples_split=5,oob_score=True)
clf.fit(train, y_train)

#predict on test data
pred_1 = clf.predict_proba(test)
# This gave accuracy around 99.8xx

#train model using gbm
import xgboost as xgb
gbm = xgb.XGBClassifier(max_depth=3, n_estimators=300, learning_rate=0.05).fit(train, y_train)
pred_2 = gbm.predict_proba(test)
# This gave accuracy around 99.9xx

# Since gbm had higher accuracy, I gave it higher weightage
pred = 0.80*pred_2+0.20*pred_1


#write submission file and submit
columns = ['Front','Left','Rear','Right']
sub = pd.DataFrame(data=pred, columns=columns)
sub['Id'] = test_id
sub = sub[['Id','Front','Left','Rear','Right']]
sub.to_csv("sub_0.8xgboost_0.2rf.csv", index=False)
