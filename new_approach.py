import pickle
import pandas as pd
from BFS import Graph
from pairwise_corr import read_nmf_data, compute_coor
#from pyvis.network import Network
from tqdm import tqdm
#from collections import defaultdict
import os
import multiprocessing

def calc_corr(week):
    filename = "DataSet/nmf/nmf-for-week-{}.pkl".format(week)
    
    # NMF-> compute pairwise -> find clusters
    users, values = read_nmf_data(filename)
    data = compute_coor(values) #return correlation matrix
    return data, users

def save_corr(week,data, users):
    data_dict = {}
    for i in range(len(data)-1):
        for j in range(i+1, len(data)):
            if data_dict.get(users[i], None) is None:
                data_dict[users[i]] = {}
            if data_dict.get(users[j], None) is None:
                data_dict[users[j]] = {}
            data_dict[users[i]][users[j]] = data[i][j]
            data_dict[users[j]][users[i]] = data[j][i]

    with open("DataSet/correlation/correlation-for-week-{}.pkl".format(week), "wb") as corr_f:
        pickle.dump((data_dict), corr_f)
    return None

def calc_corr_and_save(week):
    data, users = calc_corr(week)
    #save_corr(week, data, users)
    return data, users

def calc_clusters(week): 

    try:
        f1 = open("DataSet/correlation/correlation-for-week-{}.pkl".format(week), "rb")
        f1.close()
        print("Correlation for week {} exists... omitting".format(week))
    except FileNotFoundError:
        print("Calculating correlation for week {}".format(week))
        data, users = calc_corr_and_save(week)
        print("Calculating clusters for week {}".format(week))
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
        root = 0
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
        
        botnames = pd.read_csv("botnames.csv")
        week_bots = set(botnames["BotName"].tolist()).intersection(set(users))
        calculated_bots = set()
        for idx, cluster in enumerate(named_clusters): 
            cluster_set = set(cluster) 
            cluster_bots = cluster_set.intersection(week_bots) 
            calculated_bots.update(cluster_bots) 

        with open("DataSet/new_approach/new_approach-for-week-{}.pkl".format(week), "wb") as cluster_f:
            pickle.dump((named_clusters,calculated_bots, len(calculated_bots)/len(week_bots)), cluster_f)
        print("Done for week {}".format(week))
        return [] 


def main():
    number_of_files = len(os.listdir('DataSet/nmf'))
    pool = multiprocessing.Pool(processes=20)
    #results = [pool.apply_async(calc_node2vec, args=(week,)) for week in range(1,number_of_files+1)]
    results = [pool.apply_async(calc_clusters, args=(week,)) for week in range(6, 12)]
    for p in results:
        p.get()
    pool.close()
    pool.terminate()
    pool.join()
    
if __name__ == '__main__':
    main()
