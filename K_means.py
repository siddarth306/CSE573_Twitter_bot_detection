import csv
import os
import os.path
from pairwise_corr import read_nmf_data, compute_coor_for_cluster
from sklearn.cluster import KMeans
import pandas as pd

# Runs K means and finds the the optimal k using elbow method
# ref: https://blog.cambridgespark.com/how-to-determine-the-optimal-number-of-clusters-for-k-means-clustering-14f27070048f
def find_optimal_k(data):
    # import matplotlib.pyplot as plt
    Sum_of_squared_distances = []
    K = range(1, 30)
    for k in K:
        km = KMeans(n_clusters=k)
        km = km.fit(data)
        Sum_of_squared_distances.append(km.inertia_)

    # # Graph figure
    # plt.plot(K, Sum_of_squared_distances, 'bx-')
    # plt.xlabel('k')
    # plt.ylabel('Sum_of_squared_distances')
    # plt.title('Elbow Method For Optimal k')
    # plt.show()

    # find elbow
    from kneed import KneeLocator
    kn = KneeLocator(K, Sum_of_squared_distances, curve='convex', direction='decreasing')
    print(kn.knee)
    return kn


def find_bots(clusters_of_username, users):
    #   :param      - clusters_of_username = [["user1","user2"],["user9"]]
    #   :returns    - bots_in_cluster = [{"user1"},{}]

    # # read botnames.csv
    botnames = pd.read_csv("/home/smollfish/Desktop/CSE573_Twitter_bot_detection/DataSet/botnames.csv")
    week_bots = set(botnames["BotName"].tolist()).intersection(set(users))

    # compare clusters to bot list: for each cluster
    set_b = set(botnames)
    bots_in_cluster = []
    for i in range(len(clusters_of_username)):
        set_a = set(clusters_of_username[i])
        bots = set_a.intersection(week_bots)
        bots_in_cluster.append(bots)

    return bots_in_cluster


def run_kmeans(filepath, ith):
    print("Reading...", filepath)
    users, values = read_nmf_data(filepath)

    # optimal_k = find_optimal_k(values)
    # n_cluster = optimal_k.elbow
    optimal_k = best_k_precomputed[ith]

    # cluster data
    n_cluster = optimal_k
    kmeans = KMeans(n_clusters=n_cluster, random_state=0).fit(values)

    # find the users in each cluster + count the data points in each cluster
    clusters_of_users = [[] for k in range(n_cluster)]
    clusters_of_values = [[] for k in range(n_cluster)]  # NMF data corresponding to clusters_of_users
    for i in range(len(kmeans.labels_)):
        clusters_of_users[kmeans.labels_[i]].append((users[i]))
        clusters_of_values[kmeans.labels_[i]].append(values[i])
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
    print("Average Accuracy: ", calculated_bots / len(week_bots))
    print()


best_k_precomputed = [9, 3, 4, 4, 6, 4, 4, 6, 4, 4, 5, 4, 2, 4, 5, 5, 8, 3, 6, 4, 7, 6, 7, 6, 5, 4, 3, 5, 3, 6, 3, 3, 5,
                      4, 3, 4]

def main():
    basepath = "/home/smollfish/Desktop/CSE573_Twitter_bot_detection/"
    print('Reading data from nmf folder...')
    number_of_files = len(os.listdir(basepath + 'DataSet_filtered/nmf'))
    for index in range(15
            , number_of_files + 1):
        filepath = os.path.join(basepath, 'DataSet_filtered', 'nmf', 'nmf-for-week-' + str(index) + '.pkl')
        run_kmeans(filepath, index - 1)


if __name__ == '__main__':
    main()
