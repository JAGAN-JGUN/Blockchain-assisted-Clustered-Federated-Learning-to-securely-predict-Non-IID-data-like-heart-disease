# Simple example to check for data drift
from scipy.stats import ks_2samp
import pandas as pd

X_initial = pd.read_csv("batch_1.csv")
X_initial = X_initial[['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal']]
X_new = pd.read_csv("train.csv")
X_new = X_new[['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal']]
def check_data_drift(initial_data, new_data):
    drift_detected = []
    for col in initial_data.columns:
        stat, p_value = ks_2samp(initial_data[col], new_data[col])
        if p_value < 0.05:
            drift_detected.append(col)
    return drift_detected

drift_features = check_data_drift(X_initial, X_new)
print("Features with data drift:", drift_features)
