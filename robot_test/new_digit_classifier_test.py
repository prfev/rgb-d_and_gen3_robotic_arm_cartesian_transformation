import numpy as np # linear algebra
import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA, KernelPCA
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.neighbors import KNeighborsClassifier as KNC 
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

data = pd.read_csv(r'C:\Users\prfev\Desktop\TCC_Scripts\tcc_finals\robot_test\train.csv')
X = data.drop(columns='label').to_numpy()
y = data['label'].to_numpy()

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2)
X_train.shape, X_test.shape, y_train.shape, y_test.shape

plt.imshow(X_train[0,:].reshape((28,28)))
plt.show()

digit_container = {}
for i in range(len(y_train)):
    digit_container[i] = X_train[y_train == i,:]
    digit_container[i] = digit_container[i].T

U_container = []
for i in range(10):
    U, S, VT = np.linalg.svd(digit_container[i],full_matrices=False)
    U_container.append(U)
    plt.figure(i)
    plt.plot(np.cumsum(S)/np.sum(S),c='red')
    plt.title(f'Singular values U{i} : cumulative sum U{i}')
    plt.show()

y_pred1 = np.array([])
for i in range(len(X_test)):
    dis = np.inf
    yp = 0
    for k in range(10):
        d = np.linalg.norm((np.eye(28*28) - U_container[k][:,:20] @ U_container[k][:,:20].T) @ X_test[i,:])
        if d < dis:
            dis = d
            yp = k
    y_pred1 = np.concatenate((y_pred1,[yp]))

step2 = [
    ('transformer',PCA(n_components=100)),
    ('classifier',RFC(n_estimators=10))
        ]

step3 = [
    ('transformer',PCA(n_components=100)),
    ('classifier',KNC(n_neighbors=5))    
]

step4 = [
    ('transformer',PCA(n_components=100)),
    ('classifier',SVC())
]

clf2 = Pipeline(steps=step2)
clf3 = Pipeline(steps=step3)
clf4 = Pipeline(steps=step4)

clf2.fit(X_train,y_train)


clf3.fit(X_train,y_train)
clf4.fit(X_train,y_train)



y_pred2 = clf2.predict(X_test)
y_pred3 = clf3.predict(X_test)
y_pred4 = clf4.predict(X_test)

print(f'SVD digits accuracy : {accuracy_score(y_test,y_pred1)}')
print(f'Random Forest Classifier accuracy : {accuracy_score(y_test,y_pred2)}')
print(f'KNeighbors Classifier accuracy : {accuracy_score(y_test,y_pred3)}')
print(f'SVM accuracy : {accuracy_score(y_test,y_pred4)}')



