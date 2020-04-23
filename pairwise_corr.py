import K_means as km
import pandas as pd
import pickle

def read_nmf_data(filename):
    dict = pickle.load(open(filename, 'rb'))
    # convert dict to array
    users = []
    values = []
    for key in dict:
        users.append(key)
        values.append(dict[key])
    return users, values

def compute_coor(data):
    df = pd.DataFrame(data).transpose()
    coor_matrix = df.corr(method='pearson')
    coor_matrix[coor_matrix < .90] = 0 #filter
    return coor_matrix




