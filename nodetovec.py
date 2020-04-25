import os
import os.path

import networkx as nx
import pandas as pd
from node2vec import Node2Vec


def node_2_vec(graph):
    node2vec = Node2Vec(graph, dimensions=64, walk_length=30, num_walks=200, workers=1)
    model = node2vec.fit(window=10, min_count=2)
    print(model)
    for node in model:
        if len(node) > 3:
            print(node)


def construct_graph(data):
    nodes = []
    edges = []
    seen = set()
    graph = nx.Graph()
    for key1, value1 in data.items():
        nodes.append(key1)
        for key2, value2 in data.items():
            if key1 != key2 and key2 not in seen:
                if len(value1 & value2) >= 2:
                    pair = (key1, key2)
                    edges.append(pair)
        seen.add(key1)
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    print(graph.nodes())
    print(graph.edges())
    return graph


def main():
    print('Reading data from users folder...')
    number_of_files = len(os.listdir('DataSet/users'))
    for index in range(1, number_of_files + 1):
        data = pd.read_pickle(os.path.join('DataSet', 'users', 'data-from-week-' + str(index) + '.pkl'))
        print("Done Reading...")
        graph = construct_graph(data)
        print("made graph...")
        node_2_vec(graph)


if __name__ == '__main__':
    main()
