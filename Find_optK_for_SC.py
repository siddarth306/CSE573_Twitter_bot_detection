from scipy.sparse import csgraph
from numpy import linalg as LA
import matplotlib.pyplot as plt
import numpy as np
from pairwise_corr import read_nmf_data, compute_coor

def eigenDecomposition(A, plot=True, topK=5):
    """
    :param A: Affinity matrix
    :param plot: plots the sorted eigen values for visual inspection
    :return A tuple containing:
    - the optimal number of clusters by eigengap heuristic
    - all eigen values
    - all eigen vectors

    This method performs the eigen decomposition on a given affinity matrix,
    following the steps recommended in the paper:
    1. Construct the normalized affinity matrix: L = D−1/2ADˆ −1/2.
    2. Find the eigenvalues and their associated eigen vectors
    3. Identify the maximum gap which corresponds to the number of clusters
    by eigengap heuristic

    References:
    https://papers.nips.cc/paper/2619-self-tuning-spectral-clustering.pdf
    http://www.kyb.mpg.de/fileadmin/user_upload/files/publications/attachments/Luxburg07_tutorial_4488%5b0%5d.pdf
    """
    L = csgraph.laplacian(A, normed=True)
    n_components = A.shape[0]

    # LM parameter : Eigenvalues with largest magnitude (eigs, eigsh), that is, largest eigenvalues in 
    # the euclidean norm of complex numbers.
    #     eigenvalues, eigenvectors = eigsh(L, k=n_components, which="LM", sigma=1.0, maxiter=5000)
    eigenvalues, eigenvectors = LA.eig(L)

    # if plot:
    #     plt.title('Largest eigen values of input matrix')
    #     plt.scatter(np.arange(len(eigenvalues)), eigenvalues)
    #     plt.grid()

    # Identify the optimal number of clusters as the index corresponding
    # to the larger gap between eigen values
    index_largest_gap = np.argsort(np.diff(eigenvalues))[::-1][:topK]
    nb_clusters = index_largest_gap + 1

    return nb_clusters, eigenvalues, eigenvectors


# sample_filename = "/home/smollfish/Desktop/CSE573_Twitter_bot_detection/DataSet_filtered/nmf/nmf-for-week-2.pkl"
# users, values = read_nmf_data(sample_filename)
# coor_matrix= compute_coor(values)
# print(coor_matrix)
# nb_clusters, eigenvalues, eigenvectors=eigenDecomposition(coor_matrix.to_numpy())
# print(min(nb_clusters))