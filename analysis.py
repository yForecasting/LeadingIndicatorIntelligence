import os
import math
# Essential Libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# Preprocessing
from sklearn.preprocessing import MinMaxScaler
# Algorithms
from minisom import MiniSom
from tslearn.barycenters import dtw_barycenter_averaging
from tslearn.clustering import TimeSeriesKMeans
from sklearn.cluster import KMeans
from collections import Counter
from sklearn.decomposition import PCA
from statistics import variance, stdev, mean
csv = pd.read_csv("monthly_data.csv")
csv = csv.drop("date", axis=1)


def nan_counter(list_of_series):
    nan_polluted_series_counter = 0
    for series in list_of_series:
        series = list_of_series[series]
        if series.isnull().sum().sum() > 0:
            nan_polluted_series_counter += 1


csv.interpolate(limit_direction="both", inplace=True)
nan_counter(csv)
names = csv
scaler = MinMaxScaler()
csv = MinMaxScaler().fit_transform(csv)
som_x = som_y = math.ceil(math.sqrt(math.sqrt(len(csv))))
csv = np.transpose(csv)
# I didn't see its significance but to make the map square,
# I calculated square root of map size which is
# the square root of the number of series
# for the row and column counts of som

som = MiniSom(som_x, som_y, len(csv[0]), sigma=0.3, learning_rate=0.1)

som.random_weights_init(csv)
som.train(csv, 50000)


def plot_som_series_dba_center(som_x, som_y, win_map):
    fig, axs = plt.subplots(som_x, som_y, figsize=(25, 25))
    fig.suptitle('Clusters')
    for x in range(som_x):
        for y in range(som_y):
            cluster = (x, y)
            if cluster in win_map.keys():
                for series in win_map[cluster]:
                    axs[cluster].plot(series, c="gray", alpha=0.5)
                axs[cluster].plot(dtw_barycenter_averaging(np.vstack(win_map[cluster])), c="red")  # I changed this part
            cluster_number = x * som_y + y + 1
            axs[cluster].set_title(f"Cluster {cluster_number}")

    plt.show()

win_map = som.win_map(csv)

cluster_c = []
cluster_n = []
for x in range(som_x):
    for y in range(som_y):
        cluster = (x, y)
        if cluster in win_map.keys():
            cluster_c.append(len(win_map[cluster]))
        else:
            cluster_c.append(0)
        cluster_number = x * som_y + y + 1
        cluster_n.append(f"Cluster {cluster_number}")



cluster_map = []
i = 0
cluster_x = []
cluster_dict = {}
for idx in names:
    winner_node = som.winner(csv[i])
    name = f"Cluster {winner_node[0] * som_y + winner_node[1] + 1}"
    cluster_map.append((idx, name))

    cluster_x.append(name)
    i += 1

cluster_x = Counter(cluster_x)
clusters = pd.DataFrame(cluster_map, columns=["Name", "Cluster"]).sort_values(by="Cluster").set_index("Cluster")
print(clusters)
plt.figure(figsize=(25, 5))
plt.title("Number of data columns in each cluster")
plt.bar(cluster_x.keys(), cluster_x.values())
plt.show()
datas = []
means = []
for name in clusters.loc[cluster_x.most_common()[0][0]]["Name"].values:
    data = names[name].values
    datas += list(data)
    means.append(mean(list(data)))
print(stdev(datas))
print(stdev(means))
