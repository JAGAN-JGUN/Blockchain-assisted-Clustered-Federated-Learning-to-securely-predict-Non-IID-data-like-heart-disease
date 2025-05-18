import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import pickle
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

train_data = pd.read_csv("train.csv")

X_train = train_data[['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal']]

Y_train = train_data['target']

mms = MinMaxScaler()
X_train = mms.fit_transform(X_train)

convert = {"Absence" : 0,"Presence" : 1}
Y_train=Y_train.replace(convert)

lr = SGDClassifier(loss="log_loss", warm_start=True, max_iter=100, tol=1e-4, shuffle=False)
lr.fit(X_train,Y_train)

for i in range(1, 5):
    test_data = pd.read_csv(f"test_{i}_dataset.csv")

    X_test = test_data[['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal']]
    Y_test = test_data['target']

    X_test = mms.fit_transform(X_test)
    Y_test=Y_test.replace(convert)

    Y_pred = lr.predict(X_test)

    cm = confusion_matrix(Y_test,Y_pred)
    print(cm)

    plt.matshow(cm, cmap=plt.cm.binary, interpolation='nearest',)
    plt.title(f'Traditional LR - {i}')
    plt.colorbar()
    plt.ylabel('expected label')
    plt.xlabel('predicted label')
    plt.show()

    accuracy = accuracy_score(Y_test, Y_pred)
    precision = precision_score(Y_test, Y_pred, average='weighted')
    recall = recall_score(Y_test, Y_pred, average='weighted')
    f1 = f1_score(Y_test, Y_pred, average='weighted')

    print(f"Accuracy: {accuracy}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1 Score: {f1}")

filename = 'global_model.pkl'
params = {'coef' : lr.coef_, 'intercept' : lr.intercept_}
pickle.dump(params, open(filename, 'wb'))