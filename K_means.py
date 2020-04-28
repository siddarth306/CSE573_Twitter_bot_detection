import csv
import os
import os.path
from pairwise_corr import read_nmf_data
from sklearn.cluster import KMeans

# sample_filename = "/home/smollfish/Desktop/CSE573_Twitter_bot_detection/DataSet_filtered/nmf/nmf-for-week-1.pkl"


# Runs K means and finds the the optimal k using elbow method
# ref: https://blog.cambridgespark.com/how-to-determine-the-optimal-number-of-clusters-for-k-means-clustering-14f27070048f
def find_optimal_k(data):
    Sum_of_squared_distances = []
    K = range(1, 30)
    for k in K:
        km = KMeans(n_clusters=k)
        km = km.fit(data)
        Sum_of_squared_distances.append(km.inertia_)

    # Graph figure
    # plt.plot(K, Sum_of_squared_distances, 'bx-')
    # plt.xlabel('k')
    # plt.ylabel('Sum_of_squared_distances')
    # plt.title('Elbow Method For Optimal k')
    # plt.show()

    #find elbow
    from kneed import KneeLocator
    kn = KneeLocator(K, Sum_of_squared_distances, curve='convex', direction='decreasing')
    print(kn.knee)
    return kn

#i.e. input should look like
#   clusters_of_username = [["user1","user2"],["user9"]]
#   returns bots_in_cluster = [{"user1"},{}]
def find_bots(clusters_of_username):
    # read botnames.csv
    with open('DataSet/botnames.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        botnames = []
        for row in readCSV:
            botnames.append(row[1])
    del botnames[0]  # remove first row, this was the title of the csv column

    # compare clusters to bot list: for each cluster, what is the ratio of bots to other users
    set_b = set(botnames)
    bots_in_cluster = []
    for i in range(len(clusters_of_username)):
        set_a = set(clusters_of_username[i])
        bots = set_a.intersection(set_b)
        bots_in_cluster.append(bots)

    return bots_in_cluster

# will organize code better, and rename this function later
def run_kmeans(filepath):
    print("Reading...", filepath)
    users, values = read_nmf_data(filepath)
    optimal_k = find_optimal_k(values)

    # cluster data
    n_cluster = optimal_k.elbow
    kmeans = KMeans(n_clusters=n_cluster, random_state=0).fit(values)

    # find the users in each cluster + count the data points in each cluster
    clusters_of_users = [[] for k in range(n_cluster)]
    clusters_of_values = [[] for k in range(n_cluster)]  # NMF data corresponding to clusters_of_users
    for i in range(len(kmeans.labels_)):
        clusters_of_users[kmeans.labels_[i]].append(users[i])
        clusters_of_values[kmeans.labels_[i]].append(values[i])

    print("Number of users in each cluster k={:}:".format(n_cluster),
          [len(clusters_of_users[k]) for k in range(n_cluster)])

    # find bots in each cluster
    bots_in_cluster = find_bots(clusters_of_users)
    print("Number of bots in each cluster k={:}:".format(n_cluster),
          [len(bots_in_cluster[k]) for k in range(n_cluster)])

    # calculate precision of each cluster
    precision_of_clusters = []
    [precision_of_clusters.append(len(bots_in_cluster[k]) / len(clusters_of_users[k])) for k in range(n_cluster)]
    average_precision = sum(precision_of_clusters) / len(precision_of_clusters)
    print("Average Precision:", average_precision, "\n")

    return clusters_of_values, optimal_k


def main():
    basepath = "/home/smollfish/Desktop/CSE573_Twitter_bot_detection/"
    print('Reading data from nmf folder...')
    number_of_files = len(os.listdir(basepath + 'DataSet_filtered/nmf'))
    for index in range(1, number_of_files + 1):
        filepath = os.path.join(basepath, 'DataSet_filtered', 'nmf', 'nmf-for-week-' + str(index) + '.pkl')
        run_kmeans(filepath)


if __name__ == '__main__':
    main()
