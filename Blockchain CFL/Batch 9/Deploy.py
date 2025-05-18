import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
import warnings
from sklearn.preprocessing import MinMaxScaler
warnings.simplefilter('ignore')
from web3 import Web3
import json

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
assert w3.is_connected(), "Web3 connection failed"

# Get the first account from Ganache
account = w3.eth.accounts[9]

# Load compiled contract ABI and Bytecode
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
    coefs = [int(x) for x in coefs[0]]
    intercept = int(intercept*10**8)
    contract = w3.eth.contract(address=contract_address, abi=abi)
    tx = contract.functions.setModelParameters(coefs, intercept).transact({"from": account})
    w3.eth.wait_for_transaction_receipt(tx)

def get_parameters(address):
    contract = w3.eth.contract(address=address, abi=abi)
    coefs, intercept = contract.functions.getModelParameters().call()
    return coefs, intercept

class NodeClient:
    def __init__(self, client_id):
        self.client_id = client_id

    def train_model(self):
        data = pd.read_csv(f'batch_{self.client_id}.csv')
        X = data[['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal']]
        Y = data['target']

        mms = MinMaxScaler()
        X = mms.fit_transform(X)

        with open("address_get.txt", "r") as file:
            for line in file:
                address = line.strip()
                coefs, intercept = get_parameters(address)
                coefs = np.array(coefs)*10**-8
                intercept = intercept*10**-8

        model = LogisticRegression(max_iter=100)
        
        dummy_X = np.zeros((2, coefs.shape[0]))
        dummy_y = np.array([0, 1])
        model.fit(dummy_X, dummy_y)

        model.coef_ = coefs
        model.intercept_ = intercept
        
        model.fit(X, Y)

        set_parameters(model.coef_, model.intercept_)

if __name__ == "__main__":
    client = NodeClient(client_id=2)
    client.train_model()