#
# The code is very messy. I'll clean it later.
#
#


import pickle
from sklearn.decomposition import NMF
import multiprocessing
import numpy as np
import sys
import os


def calc_np_matrix(week, tool_config):
    print("Computing np matrix for week {}".format(week))
    week_f = open(tool_config["weeks_dir"].format(week), "rb")
    
    week_data = pickle.load(week_f)
    max_vector_size = len(week_data["retweet_tid"].unique())
    
    f1 = open(tool_config["user_vector_dir"].format(week), "rb")
    data = pickle.load(f1)
    f1.close()
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
    print("Saving np matrix")
    with open(tool_config["np_dir"].format(week), "wb") as np_f1:
        pickle.dump(np_mat, np_f1)
    return []


def calc_NMF_matrix(week, tool_config):
    try:
        f = open(tool_config["nmf_dir"].format(week), "r")
        f.close()
        print("file " + tool_config["nmf_dir"].format(week) + " exists.. ignoring")
        return []
    except FileNotFoundError:
        pass

    with open(tool_config["np_dir"].format(week), "rb") as np_f1:
        np_mat = pickle.load(np_f1)
    if len(np_mat) == 0:
        return []
    f1 = open(tool_config["user_vector_dir"].format(week), "rb")
    data = pickle.load(f1)
    f1.close()
    users = list(data.keys())
 
    print("Computing NMF for week {}".format(week))
    
    model = NMF(n_components=50, init='random', random_state=0)
    W = model.fit_transform(np_mat)

    NMF_dict = {}

    for idx, name in enumerate(users):
        NMF_dict[name] = W[idx]

    nmf_f = open(tool_config["nmf_dir"].format(week), "wb")
    pickle.dump(NMF_dict, nmf_f)
    print("Finished {}".format(week))
    return []

def main():
    if len(sys.argv) != 2:
        timeperiod = 1
    else:
        timeperiod = int(sys.argv[1])

    BASE_DIR = "./DataSet_{}_day/".format(timeperiod)
    tool_config = {
        "base_dir": BASE_DIR,
        "user_vector_dir": BASE_DIR + "vectors/user-vectors-for-week-{}.pkl",
        "nmf_dir" : BASE_DIR + "nmf/nmf-for-week-{}.pkl",
        "np_dir": BASE_DIR + "numpy_matrices/np-for-week-{}.pkl",
        "weeks_dir": BASE_DIR + "weeks/data-from-week-{}.pkl",
    }
    count = len([name for name in os.listdir(tool_config["base_dir"] + "vectors") if ".pkl" in name])

    #week = sys.argv[1]
    #weeks_range = range(11,37)
    #for week in weeks_range:
    #    calc_NMF_matrix(week)
    #pool = multiprocessing.Pool(processes=3)
    #results = [pool.apply_async(calc_np_matrix, args=(week,tool_config)) for week in range(1,count+1)]
    #output = [p.get() for p in results]
    pool = multiprocessing.Pool(processes=3)
    results = [pool.apply_async(calc_np_matrix, args=(week,tool_config)) for week in range(1,count+1)]
    output = [p.get() for p in results]


    pool = multiprocessing.Pool(processes=3)
    results = [pool.apply_async(calc_NMF_matrix, args=(week,tool_config)) for week in range(1,count+1)]
    output = [p.get() for p in results]


if __name__ == "__main__":
    main()
