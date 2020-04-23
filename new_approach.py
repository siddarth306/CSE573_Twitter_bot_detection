import pickle
import pandas as pd
from BFS import Graph
from pairwise_corr import read_nmf_data, compute_coor
from pyvis.network import Network

sample_filename = "nmf-for-week-1.pkl"

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
for i in range(0, len(data)):
    for j in range(0, len(data)):
        if (data[i][j] != 0):
            g.addEdge(i, j)

#find clusters
clusters=[]
root=0
nodes = set(range(0, len(data))) # need this list so i can find the next nodes to run BFS on

while (1):
    nodes_visited = g.BFS(root)
    if len(nodes_visited) == 0:
        break
    clusters.append(nodes_visited)
    print(nodes_visited)
    g.removeNodes(nodes_visited) # remove nodes visited graph

    nodes = nodes-set(nodes_visited)
    if len(nodes)==0: #ran out of nodes
        break;
    root = list(nodes)[0] #get first item

print(clusters)



