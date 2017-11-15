
# coding: utf-8

# In[ ]:




# In[7]:

import pandas as pd
from sklearn.utils import shuffle
from sklearn.feature_selection import VarianceThreshold,SelectKBest,chi2,RFE
import numpy as np
from sklearn.svm import SVC
# from sklearn.cross_validation import KFold
from sklearn.model_selection import train_test_split,KFold
from sklearn.metrics import precision_score
from sklearn.decomposition import LatentDirichletAllocation
from sklearn import preprocessing
from sklearn.metrics.cluster import v_measure_score
from sklearn.preprocessing import normalize


file_name = 'network_prob.csv'
#file_name = 'network.csv'
df = pd.read_csv(file_name)
df = df.dropna(axis = 0) # 'float' object has no attribute 'split'
df = df.dropna(axis = 1)
def get_network(x):
   name = x.split('_')[0]
   return name

#feature = ['network','std_cc','mean_cl','M_bc','M_ds','m_sv','m_ds','std_cl','prob']
#feature = ['network','std_cc','mean_cl','M_bc','M_ds','m_sv','m_ds','m_cl','std_cl','prob']
feature_pure =['network','std_cc', 'M_cl' ,'M_ds', 'm_bc' ,'mean_cl', 'M_bc' ,'std_cl' ,'std_ds','prob' ]
df['network'] = df.network.apply(get_network)
df_pure = df.iloc[0:800,:]
df_hybrid = df.iloc[1200:,:]
df_pure = df_pure.loc[:,feature_pure]
#df_hybrid = df_hybrid.loc[:,feature]
#df_hybrid = df_hybrid.loc[lambda df_hybrid: df_hybrid.prob == 0.3, :] #hybrid percentage
df_pure = shuffle(df_pure, random_state=7)
df_hybrid = shuffle(df_hybrid, random_state=7)



# In[8]:

X = df_pure.drop('network',1)
# X = df_hybrid.drop('network',1)
X = X.drop('prob',1)
Xnorm = (X - X.min()) / (X.max() - X.min())
X = Xnorm
    
#y = np.array(df_hybrid['network'])
#y_prob = np.array(df_hybrid['prob'])
y = np.array(df_pure['network'])
#print (df_hybrid)
#X.isnull()
#print (X)


# In[12]:

from sklearn.metrics.cluster import v_measure_score
#for k in [4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100]:
#for k in [4,5,6,7,8]:
n_topics = 4
for i in [0.5,0.6,0.7,0.8,0.9]:
    for j in [10,15,20,30,40,50]:
        lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=30,learning_decay=i,learning_offset=j, learning_method='online',random_state=7,mean_change_tol=1e-3)
        #lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=30,learning_decay=0.5,learning_offset=10, learning_method='batch',random_state=7,mean_change_tol=1e-3,batch_size=90)
        lda.fit(X)
        #print (lda.perplexity(X))
        result_matrix = lda.transform(X)
        y_pred = []
        for network in result_matrix:
            type = np.argmax(network)
            y_pred.append(type)
        # y1={}
        # for i in range (800):
        #     if y[i] not in y1.keys():
        #         y1[y[i]]=[i]
        #     else:
        #         y1[y[i]].append[i]
        # print (y1)

        le = preprocessing.LabelEncoder()
        y_transform = le.fit_transform(y)
        y_transform=y_transform.tolist()
        #     print ("V_score of Pure Network is")
        #     print ("V_score of 5% Hybrid Network is")
        print ("i %s j %svmeasure_score %s" % (i,j, v_measure_score(y_transform,y_pred)))
        #print ("k %s i %s j %s vmeasure_score %s" % (k,i,j,v_measure_score(y_transform,y_pred)))
#print (v_measure_score(y_transform,y_pred))
    #print (len(y_transform)-len(y_pred))
#print (y_transform[0:50])
#print (y_pred[0:50])


# In[306]:

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA as sklearnPCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.datasets.samples_generator import make_blobs
from pandas.tools.plotting import parallel_coordinates
y_transform = le.fit_transform(y)
# df_hybrid = df_hybrid.drop('prob',1)
# y_plot = df_hybrid['network']
# X_plot = df_hybrid.ix[:,'std_cc':]
df_pure =df_pure.drop('prob',1)
y_plot = df_pure['network']
X_plot = df_pure.ix[:,'mean_bc':]
X_norm = (X_plot - X_plot.min())/(X_plot.max() - X_plot.min())

pca = sklearnPCA(n_components=2) #2-dimensional PCA
transformed = pd.DataFrame(pca.fit_transform(X_norm))
fig1=plt.figure()
#print (transformed)
#print (transformed[y_transform==0][0])
plt.scatter(transformed[y_transform==0][0], transformed[y_transform==0][1], label='ba', c='yellow')
plt.scatter(transformed[y_transform==1][0], transformed[y_transform==1][1], label='dd', c='red')
plt.scatter(transformed[y_transform==2][0], transformed[y_transform==2][1], label='er', c='blue')
plt.scatter(transformed[y_transform==3][0], transformed[y_transform==3][1], label='la', c='brown')
print ("1% Hybrid Actual Data")
plt.show()
fig1.savefig('pure_hybrid_actual.png', transparent=True)
y_pred =np.asarray(y_pred )
fig2=plt.figure()
print ("5% Hybrid Predicted Result")
plt.scatter(transformed[y_pred==0][0], transformed[y_pred==0][1], label='er', c='brown')
plt.scatter(transformed[y_pred==1][0], transformed[y_pred==1][1], label='dd', c='pink')
plt.scatter(transformed[y_pred==2][0], transformed[y_pred==2][1], label='ba', c='blue')
plt.scatter(transformed[y_pred==3][0], transformed[y_pred==3][1], label='la', c="red")
plt.scatter(transformed[y_pred==4][0], transformed[y_pred==4][1], label='er', c='yellow')
plt.scatter(transformed[y_pred==5][0], transformed[y_pred==5][1], label='dd', c='red')
# plt.scatter(transformed[y_pred==6][0], transformed[y_pred==6][1], label='dd', c='orange')
# plt.show()
# print ("Actual Data")
# plt.scatter(transformed[y_pred==0][0], transformed[y_pred==0][1], label='la', c='red')
# plt.scatter(transformed[y_pred==1][0], transformed[y_pred==1][1], label='class 1', c='lightgreen')
# plt.scatter(transformed[y_pred==2][0], transformed[y_pred==2][1], label='ba', c='pink')
# plt.scatter(transformed[y_pred==3][0], transformed[y_pred==3][1], label='class 2', c='blue')
# plt.scatter(transformed[y_pred==4][0], transformed[y_pred==4][1], label='er', c='blue')
# plt.scatter(transformed[y_pred==5][0], transformed[y_pred==5][1], label='dd', c='red')
# plt.scatter(transformed[y_pred==5][0], transformed[y_pred==5][1], label='dd', c='brown')

plt.show()
fig2.savefig('pure_hybrid.png', transparent=True)
# y_pred =np.asarray(y_pred )
# print ("Predicted Result")
# plt.scatter(transformed[y_pred==0][0], transformed[y_pred==0][1], label='la', c='red')
# plt.scatter(transformed[y_pred==1][0], transformed[y_pred==1][1], label='er', c='lightgreen')
# plt.scatter(transformed[y_pred==2][0], transformed[y_pred==2][1], label='dd', c='blue')
# plt.scatter(transformed[y_pred==3][0], transformed[y_pred==3][1], label='ba', c='red')
# plt.show()


# In[61]:

# from lda_gibbs import LdaSampler
# import lda_gibbs 

# matrix = np.array(df_pure)
# # print (matrix[1][0]) 
# #print (len(matrix[0]))
# for i in range (len(matrix)):
#     if matrix[i][0]=="ba":
#         matrix[i][0]=1
#     elif matrix[i][0]=="la":
#         matrix[i][0]=2
#     elif matrix[i][0]=="er":
#         matrix[i][0]=3
#     else:
#         matrix[i][0]=4
# l=[]
# for i in range(1,22):
#     l.append(i)
    
# X2 = normalize(matrix[:,l], axis=0)
# # print (len(X2[0]))
# # print (X2)
# matrix=np.concatenate(( matrix[:,[0]], X2), axis=1)
# #print (matrix)
# #matrix['network']=le.fit_transform(matrix['network'])
# lda_gibbs = LdaSampler(n_topics=n_topics, alpha=1/n_topics, beta=1/n_topics)
# lda_gibbs._initialize(matrix=matrix)
# lda_gibbs.run(matrix=matrix)
# print (lda_gibbs.gen_word_distribution())
# #result=lda_gibbs.gen_word_distribution(n_topics=n_topics, document_length=800)
# #print (lda_gibbs.phi())


# In[3]:

from GibbsLDA import Sampler
D={}
l=[]
for i in range(1,22):
    l.append(i)
matrix = np.array(df_pure)
X2 = normalize(matrix[:,l], axis=0)
matrix=np.concatenate(( matrix[:,[0]], X2), axis=1)
for i in range(800):
    D[i]=np.array(df_pure.iloc[i,:]).tolist()
indD={}
for key in D:
    indD[key]=key
vocab=0
indV={}
for i in range(800):
    for j in range(1,22):
        if D[i][j] not in indV:
            indV[D[i][j]]=vocab
            vocab+=1
lda_gibbs = Sampler(documents=D, ntopics=4,indD=indD, indV=indV, VOCABS=vocab, doc=800)
lda_gibbs.run()


# In[ ]:



