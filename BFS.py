# Python3 Program to print BFS traversal
# from a given source vertex. BFS(int s)
# traverses vertices reachable from s.
from collections import defaultdict


# This class represents a directed graph
# using adjacency list representation
class Graph:

    # Constructor
    def __init__(self):

        # default dictionary to store graph
        self.graph = defaultdict(list)

    def removeNodes(self, nodes):
        for x in nodes:
            # del self.graph[x]
            self.graph[x]=[]

    # function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

    # Function to print a BFS of graph
    def BFS(self, s, nodes_visited, data):
        #nodes visited
        #nodes_visited=[]
        members = []
        # Mark all the vertices as not visited
        #visited = [False] * (len(self.graph))

        # Create a queue for BFS
        queue = []

        # Mark the source node as
        # visited and enqueue it
        queue.append(s)
        #visited[s] = True

        nodes_visited.add(s)
        while queue:

            # Dequeue a vertex from
            # queue and print it
            s = queue.pop(0)
            # print(s, end=" ")
            members.append(s)

            # Get all adjacent vertices of the
            # dequeued vertex s. If a adjacent
            # has not been visited, then mark it
            # visited and enqueue it
            for i in self.graph[s]:
                if i not in nodes_visited and data[s][i] >= 0.98:
                    queue.append(i)
                    nodes_visited.add(i)

        return members
# # Driver code
#
# # Create a graph given in
# # the above diagram
# g = Graph()
# g.addEdge(0, 1)
# g.addEdge(0, 2)
# g.addEdge(1, 2)
# g.addEdge(2, 0)
# g.addEdge(2, 3)
# g.addEdge(3, 3)
#
# print ("Following is Breadth First Traversal"
# 				" (starting from vertex 2)")
# g.BFS(2)
