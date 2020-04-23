import snap
# http://www.graphviz.org/

#dummy data
users=["u1","u2","u3","u4"]
coor_matrix=[[1,1,0,0],
      [1,1,0,0],
      [0,0,1,1],
      [0,0,1,1]]

G1 = snap.TUNGraph.New()

# add nodes
for i in range(len(users)):
    G1.AddNode(i)

#add edges
data = coor_matrix
for i in range(0, len(data)):
    for j in range(0, len(data)):
        if (j <= i):
            continue
        else:
            if (data[i][j] != 0):
                G1.AddEdge(i, j)

snap.DrawGViz(G1, snap.gvlDot, "week1.png", "Grid 5x3")
# print("G4: Nodes %d, Edges %d" % (G1.GetNodes(), G1.GetEdges()))