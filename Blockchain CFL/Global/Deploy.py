from web3 import Web3
import json
from sklearn.linear_model import LogisticRegression
import numpy as np

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
assert w3.is_connected(), "Web3 connection failed"

account = w3.eth.accounts[0]

with open("build/contracts/LogisticRegressionModel.json", "r") as file:
    JS = json.load(file)
    abi = JS['abi']
    bytecode = JS['bytecode']

import os

def set_parameters(coefs, intercept):
    CONTRACT_ADDRESS_FILE = "contract_address.txt"

    if os.path.exists(CONTRACT_ADDRESS_FILE):
        with open(CONTRACT_ADDRESS_FILE, "r") as file:
            contract_address = file.read().strip()
        print(f"Using existing contract at: {contract_address}")

    coefs = (coefs*(10**8)).tolist()
    coefs = [int(x) for x in coefs]
    intercept = int(intercept*10**8)
    contract = w3.eth.contract(address=contract_address, abi=abi)
    tx = contract.functions.setModelParameters(coefs, intercept).transact({"from": account})
    w3.eth.wait_for_transaction_receipt(tx)

def get_parameters(address):
    contract = w3.eth.contract(address=address, abi=abi)
    coefs, intercept = contract.functions.getModelParameters().call()
    return coefs, intercept

def fed_avg(global_model):
    aggregated_coef = None
    aggregated_intercept = None
    total_clients = 0
    with open("address_get.txt", "r") as file:
        for line in file:
            address = line.strip()
            coef, intercept = get_parameters(address)
            coef = np.array(coef)*10**-8
            intercept = intercept*10**-8
            if total_clients == 0:
                aggregated_coef = np.array(coef, dtype = np.float64)
                aggregated_intercept = np.array(intercept, dtype = np.float64)
            else:
                aggregated_coef = np.add(aggregated_coef, coef)
                aggregated_intercept = np.add(aggregated_intercept, intercept)
            total_clients = total_clients + 1

    aggregated_coef /= total_clients
    aggregated_intercept /= total_clients

    dummy_X = np.zeros((2, aggregated_coef.shape[0]))
    dummy_y = np.array([0, 1])
    global_model.fit(dummy_X, dummy_y)

    global_model.coef_ = aggregated_coef
    global_model.intercept_ = aggregated_intercept

    return global_model

def fed_prox(global_model, mu=0.01):
    aggregated_coef = None
    aggregated_intercept = None
    total_clients = 0
    with open("address_get.txt", "r") as file:
        for line in file:
            address = line.strip()
            coef, intercept = get_parameters(address)
            coef = np.array(coef)*10**-8
            intercept = intercept*10**-8
            if total_clients == 0:
                aggregated_coef = np.array(coef, dtype = np.float64)
                aggregated_intercept = np.array(intercept, dtype = np.float64)
            else:
                aggregated_coef = np.add(aggregated_coef, coef)
                aggregated_intercept = np.add(aggregated_intercept, intercept)
            total_clients = total_clients + 1
            regularization = mu * (coef - aggregated_coef)
            aggregated_coef -= regularization

    aggregated_coef /= total_clients
    aggregated_intercept /= total_clients

    dummy_X = np.zeros((2, aggregated_coef.shape[1]))
    dummy_y = np.array([0, 1])
    global_model.fit(dummy_X, dummy_y)

    global_model.coef_ = aggregated_coef
    global_model.intercept_ = aggregated_intercept

    return global_model

def fed_curv(global_model, alpha=0.01):
    aggregated_coef = None
    aggregated_intercept = None
    prev_coef = None
    total_clients = 0
    with open("address_get.txt", "r") as file:
        for line in file:
            address = line.strip()
            coef, intercept = get_parameters(address)
            coef = np.array(coef)*10**-8
            intercept = intercept*10**-8
            if total_clients == 0:
                aggregated_coef = np.array(coef, dtype = np.float64)
                aggregated_intercept = np.array(intercept, dtype = np.float64)
            else:
                aggregated_coef = np.add(aggregated_coef, coef)
                aggregated_intercept = np.add(aggregated_intercept, intercept)
            total_clients = total_clients + 1
            prev_coef = aggregated_coef.copy()
            regularization = alpha * (coef - prev_coef)
            aggregated_coef -= regularization

    aggregated_coef /= total_clients
    aggregated_intercept /= total_clients

    dummy_X = np.zeros((2, aggregated_coef.shape[1]))
    dummy_y = np.array([0, 1])
    global_model.fit(dummy_X, dummy_y)

    global_model.coef_ = aggregated_coef
    global_model.intercept_ = aggregated_intercept

    return global_model

class AggregatorServer:
    def __init__(self, method = 'FedAvg', mu = 0.01):
        self.global_model = LogisticRegression(max_iter=100)
        self.method = method
        self.mu = mu

    def aggregate_models(self):
        if self.method == 'FedAvg':
            self.global_model = fed_avg(self.global_model)
        elif self.method == 'FedProx':
            self.global_model = fed_prox(self.global_model, self.mu)
        elif self.method == 'FedCurv':
            self.global_model = fed_curv(self.global_model, self.mu)

        set_parameters(self.global_model.coef_, self.global_model.intercept_)

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

if __name__ == "__main__":
    mms = MinMaxScaler()
    method = 'FedAvg'
    server = AggregatorServer(method=method)
    server.aggregate_models()

    with open("contract_address.txt", "r") as file:
        for line in file:
            address = line.strip()
            coef, intercept = get_parameters(address)
            coef = np.array([np.array(coef)*10**-8])
            intercept = np.array([intercept*10**-8])

    model = LogisticRegression()
    print(coef.shape)
    dummy_X = np.zeros((2, coef.shape[1]))
    dummy_y = np.array([0, 1])
    model.fit(dummy_X, dummy_y)

    model.coef_ = coef
    model.intercept_ = intercept

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


# example_coefs = [1.2345, 2.2345, 3.2345, 4.2345, 5.2345, 6.2345, 7.2345, 8.2345, 9.2345, 10.2345, 11.2345, 12.2345, 13.2345]
# example_coefs = [int(x * 10**8) for x in example_coefs]
# example_intercept = int(42 * 10**8)

# set_model_parameters(example_coefs, example_intercept)
# ret_coefs, ret_intercept = get_model_parameters()
# print(f"Retrieved Coefficients: {ret_coefs}")
# print(f"Retrieved Intercept: {ret_intercept}")