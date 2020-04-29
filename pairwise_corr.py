import pandas as pd
import pickle


def read_nmf_data(filename):
    data_dict = pickle.load(open(filename, 'rb'))
    # convert dict to array
    #users = []
    #values = []
    #for key in dict:
    #    users.append(key)
    #    values.append(dict[key])
    return list(data_dict.keys()), list(data_dict.values())


def compute_coor(data):
    df = pd.DataFrame(data).transpose()
    coor_matrix = df.corr(method='pearson')
    #coor_matrix[coor_matrix < .90] = 0  # filter
    #coor_matrix[coor_matrix < .90] = 0 #filter
    return coor_matrix


# used by kmeans to find average correlation of each cluster
# and remove clusters with low correlation
def compute_coor_for_cluster(data):
    if len(data) < 2:
        return 0

    df = pd.DataFrame(data).transpose()
    coor_matrix = df.corr(method='pearson')

    # calculate avg value
    total_num_corr = 0
    sum_of_corr = 0
    start = 1
    for i in range(0, len(coor_matrix)):
        for j in range(start, len(coor_matrix)):
            sum_of_corr = sum_of_corr + coor_matrix[i][j]
            total_num_corr = total_num_corr + 1
        start += 1

    avg_corr = sum_of_corr / total_num_corr
    return avg_corr
