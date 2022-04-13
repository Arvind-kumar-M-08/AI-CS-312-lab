import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

data = pd.read_csv("spambase.data",header=None)
X = data.iloc[:,:-1]
y = data.iloc[:,-1]
scale = StandardScaler()
X = scale.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# Default rbf kernel

c = 35
model = SVC(C=c)
model.fit(X_train, y_train)
print("RBF kernel training set accuracy for c = ",c," : ",100*model.score(X_train, y_train))
print("RBF kernel testing set accuracy for c = ",c," : ",100*model.score(X_test, y_test))

# Quadratic kernel

c = 30
model = SVC(kernel="poly",degree=2,C=c)
model.fit(X_train, y_train)
print("Quadratic kernel training set accuracy for c = ",c," : ",100*model.score(X_train, y_train))
print("Quadratic kernel testing set accuracy for c = ",c," : ",100*model.score(X_test, y_test))

# Linear kernel

c = 21
model = SVC(kernel="linear" ,C = c)
model.fit(X_train, y_train)
print("Linear kernel training set accuracy for c = ",c," : ",100*model.score(X_train, y_train))
print("Linear kernel testing set accuracy for c = ",c," : ",100*model.score(X_test, y_test))

