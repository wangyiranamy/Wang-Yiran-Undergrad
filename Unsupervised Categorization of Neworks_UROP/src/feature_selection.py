import numpy as np
import pandas as pd
from sklearn.cross_validation import KFold,cross_val_score,train_test_split
from sklearn import preprocessing
from sklearn.svm import SVC
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import accuracy_score,confusion_matrix
from sklearn.utils import shuffle
import matplotlib.pyplot as plt
import MRMR
from data_discretization_quantile import data_discretization


seed = 7

filename = 'network.csv'
df = pd.read_csv(filename)
df = df.dropna(axis = 0) # 'float' object has no attribute 'split'
df = df.dropna(axis = 1)
df = df.loc[:,'network':'diameter']
df_c = df.iloc[1200:,:]
df = df.iloc[0:1200,:]
df_c = shuffle(df_c,random_state=seed)
df = shuffle(df,random_state=seed)

def get_network(x):
	name = x.split('_')[0]
	return name
df['network'] = df.network.apply(get_network)
df_c['network'] = df_c.network.apply(get_network)

def get_hybrid(x):
	hybrid = x[(x.network!='sw') & (x.network!='reg')]
	return hybrid
# df = get_hybrid(df)

y = df['network']
yc = df_c['network']
X = df.drop('network',1)
Xc = df_c.drop('network',1)
features = X.columns.values


print features


def train(X,y):
    X = preprocessing.scale(X)
    labels = y.unique()
    n_folds = 10
    n_ins = len(X)
    kfold = KFold(n=n_ins,shuffle=True,n_folds=n_folds,random_state=seed)
    split = 0.3

    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=split,random_state=seed)

    def cv_optimize(clf,parameters,Xtrain,ytrain,n_folds=kfold,score='accuracy'):
        gs = GridSearchCV(clf,param_grid=parameters,cv=n_folds,scoring=score)
        gs.fit(Xtrain,ytrain)
        print 'BEST PARAMS',gs.best_params_
        best = gs.best_estimator_
        results = cross_val_score(gs.best_estimator_, Xtrain, ytrain, cv=n_folds, scoring=score)
        print("({0:.6f}) +/- ({1:.6f})".format(results.mean(), results.std()))
        return best

    svm_grid = cv_optimize(
        SVC(random_state=seed,kernel='linear'),
        parameters = {
            'C':[10]},
        Xtrain = X,ytrain = y)

    # rf_grid = cv_optimize(
    #     RandomForestClassifier(warm_start=True,random_state=seed),
    #     parameters = {
    #         'n_estimators':[100,150],
    #         'criterion':['gini'],
    #         'max_features':[5,10,20],
    #         'max_depth':[2,5,10],
    #         'bootstrap':[True]},
    #     Xtrain = X,ytrain = y)
    model = svm_grid
    model.fit(X_train,y_train)

    pred = model.predict(X_test)
    print accuracy_score(y_test,pred)
    print('Confusion matrix, without normalization')
    cm = confusion_matrix(y_test,pred)

    def plot_confusion_matrix(cm, title='Confusion matrix', cmap=plt.cm.Blues):
        plt.imshow(cm, interpolation='nearest', cmap=cmap)
        plt.title(title)
        plt.colorbar()
        tick_marks = np.arange(len(labels))
        plt.xticks(tick_marks, labels, rotation=45)
        plt.yticks(tick_marks, labels)
        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')

    print(cm)
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    print('Normalized confusion matrix')
    print(cm_normalized)
    # plt.figure()
    plot_confusion_matrix(cm_normalized, title='Normalized confusion matrix')
    # plt.show()

X = X.as_matrix()
X_discrete = data_discretization(X, 3)

features = ['std_cc','std_ds','m_ds','std_sv','M_bc','mean_cl','mean_sv','M_cc','m_cl','std_bc', 'm_bc', 'std_cl', 'M_sv', 'diameter','m_cc', 'M_cl', 'M_ds', 'mean_ds',
 'mean_cc' 'mean_bc' 'm_sv']

'''
['mean_bc' 'std_bc' 'm_bc' 'M_bc' 'mean_cc' 'std_cc' 'm_cc' 'M_cc'
 'mean_cl' 'std_cl' 'm_cl' 'M_cl' 'mean_ds' 'std_ds' 'm_ds' 'M_ds'
 'mean_sv' 'std_sv' 'm_sv' 'M_sv' 'diameter']

'''
'''
for num_fea in range(7,8):
    X_train = X[:, [5,13,14,17,3,8,16,7]]
    # X_train = X[:, [5,13,3,8,7,2,18,6,0]]
    # X_train = X[:, [5,13,3,8]]
    train(X_train,y)
'''


for num_fea in range(1,22):
    idx = MRMR.mrmr(X_discrete, y, n_selected_features=num_fea)
    print '%s number of features: %s' % (num_fea,features[idx])
    X_train = X[:, idx]
    train(X_train,y)

