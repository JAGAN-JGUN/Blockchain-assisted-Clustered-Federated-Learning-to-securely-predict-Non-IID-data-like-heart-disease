import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import AGM

class AggregatorServer:
    def __init__(self, client_ids, method = 'FedAvg', mu = 0.01):
        self.client_ids = client_ids
        self.global_model = LogisticRegression(max_iter=100)
        self.method = method
        self.mu = mu

    def aggregate_models(self):
        if self.method == 'FedAvg':
            self.global_model = AGM.fed_avg(self.client_ids, self.global_model)
        elif self.method == 'FedProx':
            self.global_model = AGM.fed_prox(self.client_ids, self.global_model, self.mu)
        elif self.method == 'FedCurv':
            self.global_model = AGM.fed_curv(self.client_ids, self.global_model, self.mu)

        params = {"coef" : self.global_model.coef_, "intercept" : self.global_model.intercept_}
        with open('global_model.pkl', 'wb') as f:
            pickle.dump(params, f)

        print("Aggregated model saved as 'global_model.pkl'.")

if __name__ == "__main__":
    mms = MinMaxScaler()
    method = 'FedAvg'
    server = AggregatorServer(client_ids=[1, 2, 3, 4], method=method)
    server.aggregate_models()

    with open('global_model.pkl', 'rb') as f:
        params = pickle.load(f)

    model = LogisticRegression()

    dummy_X = np.zeros((2, params['coef'].shape[1]))
    dummy_y = np.array([0, 1])
    model.fit(dummy_X, dummy_y)

    model.coef_ = params['coef']
    model.intercept_ = params['intercept']

    for i in range(1, 5):
        test_data = pd.read_csv(f'test_{i}_dataset.csv')
        X_test = test_data.drop(columns=['target'])
        Y_test = test_data['target']

        X_test = mms.fit_transform(X_test)

        Y_pred = model.predict(X_test)

        cm = confusion_matrix(Y_test,Y_pred)
        print(cm)

        accuracy = accuracy_score(Y_test, Y_pred)
        precision = precision_score(Y_test, Y_pred, average='weighted')
        recall = recall_score(Y_test, Y_pred, average='weighted')
        f1 = f1_score(Y_test, Y_pred, average='weighted')

        print(f"Accuracy: {accuracy}")
        print(f"Precision: {precision}")
        print(f"Recall: {recall}")
        print(f"F1 Score: {f1}")

        plt.matshow(cm, cmap=plt.cm.binary, interpolation='nearest',)
        plt.title(f'Aggregation - {method}')
        plt.colorbar()
        plt.ylabel('expected label')
        plt.xlabel('predicted label')
        plt.show()
