import pandas as pd
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import linkage, fcluster

file_path = "Cluster Fed Learning/test.csv"
df = pd.read_csv(file_path)

X = df[['fbs', 'trestbps', 'chol', 'restecg']]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

Z = linkage(X_scaled, method='ward')

num_clusters = 4
clusters = fcluster(Z, num_clusters, criterion='maxclust')

df['Cluster'] = clusters

for cluster_num in range(1, num_clusters + 1):
    cluster_df = df[df['Cluster'] == cluster_num].drop(columns=['Cluster'])
    output_file = f"Cluster Fed Learning/test_{cluster_num}_dataset.csv"
    cluster_df.to_csv(output_file, index=False)
    print(f'Cluster {cluster_num} data saved to {output_file}')