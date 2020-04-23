from pyvis.network import Network
#https://pyvis.readthedocs.io/en/latest/tutorial.html

#dummy data
users=["u1","u2","u3","u4"]
coor_matrix=[[1,1,0,0],
      [1,1,0,0],
      [0,0,1,1],
      [0,0,1,1]]
net = Network()
net.add_nodes(users, label=users)

for i in range(0, len(coor_matrix)):
    for j in range(0,  len(coor_matrix)):
        if (j <= i):
            continue
        else:
            if(coor_matrix[i][j]!=0):
                net.add_edge(users[i],users[j], label=coor_matrix[i][j])
net.toggle_physics(True)
net.show("hello_graph.html")