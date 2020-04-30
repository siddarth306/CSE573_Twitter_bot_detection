from pyvis.network import Network
import pandas as pd
from pairwise_corr import read_nmf_data

#ref: https://pyvis.readthedocs.io/en/latest/tutorial.html

# #dummy data
# users=["u1","u2","u3","u4"]
# coor_matrix=[[1,1,0,0],
#       [1,1,0,0],
#       [0,0,1,1],
#       [0,0,1,1]]

# real data
filename = "/home/smollfish/Desktop/CSE573_Twitter_bot_detection/DataSet_filtered/nmf/nmf-for-week-1.pkl"
users, values = read_nmf_data(filename)
df = pd.DataFrame(values).transpose()
coor_matrix = df.corr(method='pearson')
coor_matrix[coor_matrix < .995] = 0  # filter

net = Network()
net.add_nodes(users, label=users)

for i in range(0, len(coor_matrix)):
    for j in range(0,  len(coor_matrix)):
        if (j <= i):
            continue
        else:
            if(coor_matrix[i][j]!=0):
                net.add_edge(users[i], users[j], label=coor_matrix[i][j])
net.toggle_physics(True)
net.show("hello_graph.html")