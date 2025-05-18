import pandas as pd
import os
import math

def divide_csv_into_custom_batches(batch_counts):
    for j, num_batches in enumerate(batch_counts):
        file_path = f'cluster_{j + 1}_dataset.csv'
        
        df = pd.read_csv(file_path)
        
        batch_size = math.ceil(len(df) / num_batches)
        
        for i in range(num_batches):

            start_index = i * batch_size
            end_index = start_index + batch_size
            

            batch = df[start_index:end_index]
            
            folder_name = f'Cluster{j + 1}'
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
                
            batch_file_name = f'batch_{i + 1}.csv'
            batch.to_csv(os.path.join(folder_name, batch_file_name), index=False)

    print(f'The CSV files have been divided into batches and saved in respective Cluster folders.')

batch_counts = [2, 4, 1, 4]
divide_csv_into_custom_batches(batch_counts)
