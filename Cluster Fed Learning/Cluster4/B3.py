import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
import pickle
import warnings
from sklearn.preprocessing import MinMaxScaler
warnings.simplefilter('ignore')

class NodeClient:
    def __init__(self, client_id):
        self.client_id = client_id

    def train_model(self):
        data = pd.read_csv(f'batch_{self.client_id}.csv')
        X = data[['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal']]
        Y = data['target']

        mms = MinMaxScaler()
        X = mms.fit_transform(X)
        
        with open('../global_model.pkl','rb') as f:
            params = pickle.load(f)
        model = LogisticRegression(max_iter=100)
        
        dummy_X = np.zeros((2, params['coef'].shape[1]))
        dummy_y = np.array([0, 1])
        model.fit(dummy_X, dummy_y)

        model.coef_ = params['coef']
        model.intercept_ = params['intercept']
        
        model.fit(X, Y)

        params = {"coef": model.coef_, "intercept": model.intercept_}
        with open(f'model_{self.client_id}.pkl', 'wb') as f:
            pickle.dump(params, f)
        
        print(f"Model for client {self.client_id} trained and saved as 'model_{self.client_id}.pkl'.")

if __name__ == "__main__":
    client = NodeClient(client_id=3)
    client.train_model()
    