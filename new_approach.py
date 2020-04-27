import pickle
import pandas as pd
from BFS import Graph
from pairwise_corr import read_nmf_data, compute_coor
from pyvis.network import Network
from tqdm import tqdm

sample_filename = "/home/sid/Projects/CSE573_Twitter_bot_detection/DataSet_7_day/nmf/nmf-for-week-12.pkl"

# NMF-> compute pairwise -> find clusters
users, values = read_nmf_data(sample_filename)
data = compute_coor(values) #return correlation matrix
print(data)
# dummy data to test BFS
# users=["u1","u2","u3","u4"]
# data=[[1,1,0,0],
#       [1,1,0,0],
#       [0,0,1,1],
#       [0,0,1,1]]

# find clusters
# # nodes=3772, edges=1849808
g = Graph()
start = 1
for i in tqdm(range(0, len(data))):
    for j in range(start, len(data)):
        if (data[i][j] >= 0.995):
            g.addEdge(i, j)
            g.addEdge(j, i)
    start += 1

#find clusters
clusters=[]
root=0
nodes = set(g.graph.keys()) # need this list so i can find the next nodes to run BFS on
global_visited = set()
for node in nodes:
    if node not in global_visited:
        nodes_visited = g.BFS(node, global_visited, data)

        clusters.append(nodes_visited)
        print(nodes_visited)
        global_visited.update(nodes_visited) # remove nodes visited graph

    #nodes = nodes-set(nodes_visited)
    #if len(nodes)==0: #ran out of nodes
    #    break;
    #root = list(nodes)[0] #get first item

named_clusters = []
for cluster in clusters:
    named_single_cluster = []
    for member in cluster:
        named_single_cluster.append(users[member])
    named_clusters.append(named_single_cluster)

botnames = pd.read_csv("/home/sid/Projects/CSE573_Twitter_bot_detection/botnames.csv")
week_bots = set(botnames["BotName"].tolist()).intersection(set(users))
calculated_bots = set()
for idx, cluster in enumerate(named_clusters): 
    cluster_set = set(cluster) 
    cluster_bots = cluster_set.intersection(week_bots) 
    if len(cluster_bots) > 0: 
        print(cluster_bots) 
    calculated_bots.update(cluster_bots) 
    total = 0
    count = 0
    non_members_total = 0
    for u_idx, u in enumerate(clusters[idx][:-1]):
        for v in clusters[idx][u_idx+1:]:
            total += data[u][v]
            if data[u][v] < 0.995:
                non_members_total += 1
            count += 1

    print(len(cluster), len(cluster_bots), total/count, non_members_total, clusters[idx], cluster)

users_dict = {}
for idx, u in enumerate(users):
    users_dict[u] = idx
week_bots_ids = []
for bot in week_bots: 
    week_bots_ids.append(users_dict[bot]) 
      

import ipdb;ipdb.set_trace()
print(clusters)



