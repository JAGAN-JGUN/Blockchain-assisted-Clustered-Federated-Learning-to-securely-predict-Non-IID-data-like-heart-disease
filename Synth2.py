import numpy as np
import pandas as pd

data = pd.read_csv('heart2.csv')

def generate_synthetic_data(original_data, num_rows=100):
    synthetic_data = pd.DataFrame()


    for column in ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']:
        mean = original_data[column].mean()
        std = original_data[column].std()
        synthetic_data[column] = np.random.normal(mean, std, num_rows)
        synthetic_data[column] = synthetic_data[column].round(0)
    
    for column in ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal', 'target']:
        synthetic_data[column] = np.random.choice(original_data[column].unique(), num_rows, 
                                                  p=original_data[column].value_counts(normalize=True).values)

    for column in synthetic_data.columns:
        synthetic_data[column] = synthetic_data[column].astype(original_data[column].dtype)

    return synthetic_data

synthetic_data = generate_synthetic_data(data, num_rows=1000)

output_path = pd.concat([pd.read_csv('heart.csv'), synthetic_data], ignore_index=True)

output_path.to_csv('heart.csv', index=False)