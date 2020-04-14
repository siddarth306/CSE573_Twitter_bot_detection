#
# The code is very messy. I'll clean it later.
#
#


INPUT_DIR = "./DataSet/vectors/user-vectors-for-week-{}.pkl"
NMF_DIR = "./DataSet/nmf/nmf-for-week-{}.pkl"
NP_DIR = "./DataSet/numpy_matrices/np-for-week-{}.pkl"
WEEKS_DIR = "./DataSet/weeks/data-from-week-{}.pkl"
import pickle
from sklearn.decomposition import NMF
import multiprocessing
import numpy as np
import sys

def calc_NMF_matrix(week):
    print("Computing NMF for week {}".format(week))
    week_f = open(WEEKS_DIR.format(week), "rb")
    
    week_data = pickle.load(week_f)
    max_vector_size = len(week_data["retweet_tid"].unique())
    
    del week_f
    f1 = open(INPUT_DIR.format(week), "rb")
    data = pickle.load(f1)
    vector_matrix = []
    users = list(data.keys())
    for name in users:
        val_list = []
        val = data[name]
        for _ in range(max_vector_size+1):
            val_list.append(val & 1)
            val = val >> 1
        if val != 0:
            return []
        vector_matrix.append(val_list)

    print("Created vector matrix")
    np_mat = np.array(vector_matrix)
    del vector_matrix
    print("Running NMF")
    with open(NP_DIR.format(week), "wb") as np_f1:
        pickle.dump(np_mat, np_f1)
    #model = NMF(n_components=50, init='random', random_state=0)
    #W = model.fit_transform(np_mat)

    #NMF_dict = {}

    #for idx, name in enumerate(users):
    #    NMF_dict[name] = W[idx]

    #nmf_f = open(NMF_DIR.format(week), "wb")
    #pickle.dump(NMF_dict, nmf_f)
    #print("Finished {}".format(week))
    #return []

 
week = sys.argv[1]
#weeks_range = range(11,37)
#for week in weeks_range:
calc_NMF_matrix(week)
#pool = multiprocessing.Pool(processes=3)
#results = [pool.apply_async(calc_NMF_matrix, args=(week,)) for week in range(11,37)]
#output = [p.get() for p in results]
import ipdb;ipdb.set_trace()
