import os
from Find_optK_for_SC import eigenDecomposition
from sklearn.cluster import SpectralClustering
from K_means import find_bots
from pairwise_corr import read_nmf_data, compute_coor_for_specClust, compute_coor_for_cluster
import pandas as pd


# ref: https://towardsdatascience.com/spectral-clustering-aba2640c0d5b

# Dummy data to test clustering
# X=[[1,1,0,0],
#     [1,1,0,0],
#     [0,0,1,1],
#     [0,0,1,1]]

# sample_filename = "/home/smollfish/Desktop/CSE573_Twitter_bot_detection/DataSet_filtered/nmf/nmf-for-week-2.pkl"


def sc(filepath):
    print("Reading...", filepath)
    users, values = read_nmf_data(filepath)
    coor_matrix = compute_coor_for_specClust(values)

    # find best k
    nb_clusters, eigenvalues, eigenvectors = eigenDecomposition(coor_matrix.values)
    n_cluster = min(nb_clusters)

    #cluster
    clustering = SpectralClustering(n_clusters=n_cluster, affinity="precomputed",
                                    assign_labels="discretize", random_state=0).fit(coor_matrix)

    # find the users in each cluster + count the data points in each cluster
    clusters_of_users = [[] for k in range(n_cluster)]
    clusters_of_values = [[] for k in range(n_cluster)]  # NMF data corresponding to clusters_of_users
    for i in range(len(clustering.labels_)):
        clusters_of_users[clustering.labels_[i]].append(users[i])
        clusters_of_values[clustering.labels_[i]].append(values[i])
    print("Number of users in each cluster k={:}:".format(n_cluster),
          [len(clusters_of_users[k]) for k in range(n_cluster)])

    # find bots in each cluster
    bots_in_cluster = find_bots(clusters_of_users, users)
    print("Number of Russian bots in each cluster k={:}:".format(n_cluster),
          [len(bots_in_cluster[k]) for k in range(n_cluster)])

    # compute pairwise correlation of clusters
    avg_corr_of_clusters = []
    for cluster in clusters_of_values:
        avg_corr = compute_coor_for_cluster(cluster)
        avg_corr_of_clusters.append(avg_corr)
    [(print("Average Correlation of Cluster {:} : {:}".format(k, round(avg_corr_of_clusters[k], 2)))) for k in
     range(n_cluster)]

    # delete clusters where average correlation < .995
    for ix in range(len(avg_corr_of_clusters)):
        if (avg_corr_of_clusters[ix] < 0.90):
            clusters_of_users[ix] = []
            clusters_of_values[ix] = []

    # find bots in each cluster after removing low correlation clusters
    bots_in_cluster = find_bots(clusters_of_users, users)
    print("Number of Russian bots in each cluster after removing low correlation clusters\n",
          [len(bots_in_cluster[k]) for k in range(n_cluster)])

    # calculate precision of each cluster
    # precision 1: russian bots in each cluster/ total users in cluster
    precision_of_clusters = []
    for k in range(n_cluster):
        if len(clusters_of_users[k]) != 0:
            precision_of_clusters.append(len(bots_in_cluster[k]) / len(clusters_of_users[k]))
    if (len(precision_of_clusters) != 0):
        average_precision = sum(precision_of_clusters) / len(precision_of_clusters)
    else:
        average_precision = 0

    print("Average Cluster Precision:", average_precision)

    # precision 2: all detected russian bots/total russian bots in this week
    botnames = pd.read_csv("/home/smollfish/Desktop/CSE573_Twitter_bot_detection/DataSet/botnames.csv")
    week_bots = set(botnames["BotName"].tolist()).intersection(set(users))
    calculated_bots = 0
    for cluster in bots_in_cluster:
        calculated_bots = calculated_bots + len(cluster)

    print(
        "Total Russian bots detected: {:}, Total Russian bots in the week: {:}".format(calculated_bots, len(week_bots)))
    print("Average Russian Bot Precision: ", calculated_bots / len(week_bots))
    print()


def main():
    basepath = "/home/smollfish/Desktop/CSE573_Twitter_bot_detection/"
    print('Reading data from nmf folder...')
    number_of_files = len(os.listdir(basepath + 'DataSet_filtered/nmf'))
    for index in range(2, number_of_files + 1):
        filepath = os.path.join(basepath, 'DataSet_filtered', 'nmf', 'nmf-for-week-' + str(index) + '.pkl')
        sc(filepath)


if __name__ == '__main__':
    main()
