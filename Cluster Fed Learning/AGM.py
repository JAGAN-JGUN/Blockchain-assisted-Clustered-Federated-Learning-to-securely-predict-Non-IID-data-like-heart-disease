import numpy as np
import pickle
from sklearn.linear_model import LogisticRegression

def fed_avg(client_ids, global_model):
    total_clients = len(client_ids)
    aggregated_coef = None
    aggregated_intercept = None

    for client_id in client_ids:
        with open(f'cluster_model{client_id}.pkl', 'rb') as f:
            params = pickle.load(f)
            if aggregated_coef is None:
                aggregated_coef = np.array(params["coef"], dtype=np.float64)
                aggregated_intercept = np.array(params["intercept"], dtype=np.float64)
            else:
                aggregated_coef = np.add(aggregated_coef, params["coef"])
                aggregated_intercept = np.add(aggregated_intercept, params["intercept"])

    aggregated_coef /= total_clients
    aggregated_intercept /= total_clients

    dummy_X = np.zeros((2, aggregated_coef.shape[1]))
    dummy_y = np.array([0, 1])
    global_model.fit(dummy_X, dummy_y)

    global_model.coef_ = aggregated_coef
    global_model.intercept_ = aggregated_intercept

    return global_model

def fed_prox(client_ids, global_model, mu=0.01):
    total_clients = len(client_ids)
    aggregated_coef = None
    aggregated_intercept = None

    for client_id in client_ids:
        with open(f'cluster_model{client_id}.pkl', 'rb') as f:
            params = pickle.load(f)
            if aggregated_coef is None:
                aggregated_coef = np.array(params["coef"], dtype=np.float64)
                aggregated_intercept = np.array(params["intercept"], dtype=np.float64)
            else:
                aggregated_coef = np.add(aggregated_coef, params["coef"])
                aggregated_intercept = np.add(aggregated_intercept, params["intercept"])

            regularization = mu * (params["coef"] - aggregated_coef)
            aggregated_coef -= regularization

    aggregated_coef /= total_clients
    aggregated_intercept /= total_clients

    dummy_X = np.zeros((2, aggregated_coef.shape[1]))
    dummy_y = np.array([0, 1])
    global_model.fit(dummy_X, dummy_y)

    global_model.coef_ = aggregated_coef
    global_model.intercept_ = aggregated_intercept

    return global_model

def fed_curv(client_ids, global_model, alpha=0.01):
    total_clients = len(client_ids)
    aggregated_coef = None
    aggregated_intercept = None
    prev_coef = None

    for client_id in client_ids:
        with open(f'cluster_model{client_id}.pkl', 'rb') as f:
            params = pickle.load(f)
            if aggregated_coef is None:
                aggregated_coef = np.array(params["coef"], dtype=np.float64)
                aggregated_intercept = np.array(params["intercept"], dtype=np.float64)
                prev_coef = aggregated_coef.copy()
            else:
                aggregated_coef = np.add(aggregated_coef, params["coef"])
                aggregated_intercept = np.add(aggregated_intercept, params["intercept"])

                regularization = alpha * (params["coef"] - prev_coef)
                aggregated_coef -= regularization

    aggregated_coef /= total_clients
    aggregated_intercept /= total_clients

    dummy_X = np.zeros((2, aggregated_coef.shape[1]))
    dummy_y = np.array([0, 1])
    global_model.fit(dummy_X, dummy_y)

    global_model.coef_ = aggregated_coef
    global_model.intercept_ = aggregated_intercept

    return global_model
