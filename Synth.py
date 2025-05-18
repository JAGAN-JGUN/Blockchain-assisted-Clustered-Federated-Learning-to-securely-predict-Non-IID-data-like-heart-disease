import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE


original_data = pd.read_csv('heart.csv')
X_original = original_data.drop('target', axis=1)
y_original = original_data['target']

smote = SMOTE(random_state=42)
X_synthetic, y_synthetic = smote.fit_resample(X_original, y_original)

synthetic_data = pd.DataFrame(X_synthetic, columns=X_original.columns)
synthetic_data['target'] = y_synthetic

noise_level = 0.01
noisy_features = synthetic_data.drop('target', axis=1) + noise_level * np.random.normal(size=X_synthetic.shape)

noisy_synthetic_data = pd.concat([noisy_features, synthetic_data['target']], axis=1)

noisy_synthetic_data['age'] = noisy_synthetic_data['age'].round().astype(int)
noisy_synthetic_data['age'] = noisy_synthetic_data['age'].clip(lower=0, upper=100)
noisy_synthetic_data['sex'] = noisy_synthetic_data['sex'].apply(lambda x: 1 if x > 0.5 else 0)
noisy_synthetic_data['cp'] = noisy_synthetic_data['cp'].round().astype(int)
noisy_synthetic_data['cp'] = noisy_synthetic_data['cp'].clip(lower=0, upper=3)
noisy_synthetic_data['trestbps'] = noisy_synthetic_data['trestbps'].round().astype(int)
noisy_synthetic_data['trestbps'] = noisy_synthetic_data['trestbps'].clip(lower=90, upper=210)
noisy_synthetic_data['chol'] = noisy_synthetic_data['chol'].round().astype(int)
noisy_synthetic_data['chol'] = noisy_synthetic_data['chol'].clip(lower=120, upper=580)
noisy_synthetic_data['fbs'] = noisy_synthetic_data['fbs'].apply(lambda x: 1 if x > 0.5 else 0)
noisy_synthetic_data['restecg'] = noisy_synthetic_data['restecg'].round().astype(int)
noisy_synthetic_data['restecg'] = noisy_synthetic_data['restecg'].clip(lower=0, upper=2)
noisy_synthetic_data['thalach'] = noisy_synthetic_data['thalach'].round().astype(int)
noisy_synthetic_data['thalach'] = noisy_synthetic_data['thalach'].clip(lower=65, upper=210)
noisy_synthetic_data['exang'] = noisy_synthetic_data['exang'].apply(lambda x: 1 if x > 0.5 else 0)
noisy_synthetic_data['oldpeak'] = noisy_synthetic_data['oldpeak'].round(1)
noisy_synthetic_data['oldpeak'] = noisy_synthetic_data['oldpeak'].clip(lower=0, upper=7)
noisy_synthetic_data['slope'] = noisy_synthetic_data['slope'].round().astype(int)
noisy_synthetic_data['slope'] = noisy_synthetic_data['slope'].clip(lower=0, upper=2)
noisy_synthetic_data['ca'] = noisy_synthetic_data['ca'].round().astype(int)
noisy_synthetic_data['ca'] = noisy_synthetic_data['ca'].clip(lower=0, upper=4)
noisy_synthetic_data['thal'] = noisy_synthetic_data['thal'].round().astype(int)
noisy_synthetic_data['thal'] = noisy_synthetic_data['thal'].clip(lower=1, upper=3)

noisy_synthetic_data = pd.concat([original_data, noisy_synthetic_data], ignore_index=True)
noisy_synthetic_data.to_csv('heart.csv', index=False)