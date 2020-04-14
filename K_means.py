import pickle
import csv
from sklearn.cluster import KMeans

sample_filename = "nmf-for-week-1.pkl"

#will organize code better, and rename this function later
def get_cluster_stat(filename):
    # key = username dict.len=3772
    dict = pickle.load(open(sample_filename, 'rb'))
    # convert dict to array
    users = []
    coordinates = []
    for key in dict:
        users.append(key)
        coordinates.append(dict[key])

    # cluster data
    n_cluster = 10
    kmeans = KMeans(n_clusters=n_cluster, random_state=0).fit(coordinates)

    # find the users in each cluster + count the data points in each cluster
    clusters_of_users = [[] for k in range(n_cluster)]
    clusters_of_coordinates = [[] for k in range(n_cluster)] #need this for pair-wise correlation
    for i in range(len(kmeans.labels_)):
        clusters_of_users[kmeans.labels_[i]].append(users[i])
        clusters_of_coordinates[kmeans.labels_[i]].append(coordinates[i])

    # some print outs
    print("Number of users in each cluster k={:}:".format(n_cluster), [len(clusters_of_users[k]) for k in range(n_cluster)])

    # read botnames.csv
    with open('DataSet/botnames.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        botnames = []
        for row in readCSV:
            botnames.append(row[1])
    del botnames[0] # this was the title of the csv column

    # compare clusters to bot list: for each cluster, what is the ratio of bots to other users
    set_b = set(botnames)
    bots_in_cluster=[]
    for i in range(n_cluster):
        set_a = set(clusters_of_users[i])
        bots = set_a.intersection(set_b)
        bots_in_cluster.append(bots)
    print("Number of bots in each cluster k={:}:".format(n_cluster), [len(bots_in_cluster[k]) for k in range(n_cluster)])

    return clusters_of_coordinates
