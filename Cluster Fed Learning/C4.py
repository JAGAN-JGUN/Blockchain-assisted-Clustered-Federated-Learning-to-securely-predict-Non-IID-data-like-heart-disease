import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression
import CAGM

class AggregatorServer:
    def __init__(self, cluster_id, client_ids, method = 'FedAvg', mu = 0.01):
        self.client_ids = client_ids
        self.global_model = LogisticRegression(max_iter=100)
        self.method = method
        self.mu = mu
        self.cluster_id = cluster_id

    def aggregate_models(self):
        if self.method == 'FedAvg':
            self.global_model = CAGM.fed_avg(self.cluster_id, self.client_ids, self.global_model)
        elif self.method == 'FedProx':
            self.global_model = CAGM.fed_prox(self.cluster_id, self.client_ids, self.global_model, self.mu)
        elif self.method == 'FedCurv':
            self.global_model = CAGM.fed_curv(self.cluster_id, self.client_ids, self.global_model, self.mu)

        params = {"coef": self.global_model.coef_, "intercept": self.global_model.intercept_}
        with open(f'cluster_model{self.cluster_id}.pkl', 'wb') as f:
            pickle.dump(params, f)

        print(f'Aggregated model saved as "cluster_model{self.cluster_id}.pkl".')

if __name__ == "__main__":
    method = 'FedAvg'
    server = AggregatorServer(cluster_id = 4, client_ids=[1, 2, 3, 4], method=method)
    server.aggregate_models()
