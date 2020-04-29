
import pickle
import pandas as pd
from BFS import Graph
from pairwise_corr import read_nmf_data, compute_coor
#from pyvis.network import Network
from tqdm import tqdm
#from collections import defaultdict
import os
import multiprocessing


from gensim.models import KeyedVectors
from gensim.test.utils import get_tmpfile
from BFS import Graph

def calc_corr(week):
    filename = "DataSet/nmf/nmf-for-week-{}.pkl".format(week)
    
    # NMF-> compute pairwise -> find clusters
    users, values = read_nmf_data(filename)
    data = compute_coor(values) #return correlation matrix

    users_dict = {}
    for idx, u in enumerate(users):
        users_dict[u] = idx
    return data, users, users_dict

def calc_clusters(week):
    filepath = os.path.abspath("./DataSet/node/emb-from-week-{}.emb".format(week))
    fname = get_tmpfile(filepath)
    model = KeyedVectors.load_word2vec_format(fname)
    corr_mat, users, users_dict = calc_corr(week)
    g = Graph()
    for i in users: 
        neighbors = model.most_similar(i)   
        for n in neighbors: 
            if corr_mat[users_dict[i]][users_dict[n[0]]] > 0.99: 
                g.addEdge(i, n[0])

    #find clusters
    clusters=[]
    nodes = set(g.graph.keys()) # need this list so i can find the next nodes to run BFS on
    global_visited = set()
    for node in nodes:
        if node not in global_visited:
            nodes_visited = g.BFS(node, global_visited)
            
            if len(nodes_visited) > 1:
                clusters.append(nodes_visited)
            #print(nodes_visited)
            #global_visited.update(nodes_visited) # remove nodes visited graph
    
    botnames = pd.read_csv("botnames.csv")
    week_bots = set(botnames["BotName"].tolist()).intersection(set(users))
    calculated_bots = set()
    average_bots = 0
    for idx, cluster in enumerate(clusters): 
        cluster_set = set(cluster) 
        cluster_bots = cluster_set.intersection(week_bots) 
        calculated_bots.update(cluster_bots) 
        average_bots += len(cluster_bots) / len(cluster_set)
    #print(clusters)
    #print(len(calculated_bots)/len(week_bots), average_bots/len(clusters))

    with open("DataSet/node2vec/node2vec-for-week-{}.pkl".format(week), "wb") as cluster_f:
        pickle.dump((clusters,calculated_bots, len(calculated_bots)/len(week_bots), average_bots/len(clusters)), cluster_f)

def main():
    number_of_files = len(os.listdir('DataSet/nmf'))
    pool = multiprocessing.Pool(processes=2)
    #results = [pool.apply_async(calc_node2vec, args=(week,)) for week in range(1,number_of_files+1)]
    results = [pool.apply_async(calc_clusters, args=(week,)) for week in range(1, 3)]
    for p in results:
        p.get()
    pool.close()
    pool.terminate()
    pool.join()
    
if __name__ == '__main__':
    main()

