#导入pickle模块
import pickle
import os
# import numpy as np
# print(os.getcwd())
from sklearn.decomposition import PCA

def makeMatrix(i): # i is the nth week data
    matrix = []
    # print()
    # change path accordingly
    file = open('C:/Users/Dunchuan/PycharmProjects/573proj01/DataSet/vectors/user-vectors-for-week-' + str(i) + '.pkl', 'rb')
    pickleData = pickle.load(file)

    number = 10010
    zfnumber = "%08d" % number
    print(zfnumber)
    #result: 00010010

    maxBitLen = float('-INF')
    for user, vector in pickleData.items():
        if maxBitLen < bit_length():
            # vector = "%0d%" % vector
            print("vector is: "+ vector)

    for user, vector in pickleData.items():
        #format(vector,'0Nb')
        # print(vector.bit_length())
        #binary_string = bin(vector)
        matrix.append(binary_string)
        print(binary_string)
    return matrix

#print(len(makeMatrix(1)))

#def reduceMatrixByPCA(matrix):
#    pca = PCA(n_components=2)
#    pca.fit(matrix)

#    return matrix

m = makeMatrix(1)

print(len(m[0]), len(m[1]))
#rM = reduceMatrixByPCA(m)

# print(len(matrix[0]))
# for i in range(len(matrix)):
#     print(len(matrix[i]))
# print(len(matrix))
# m = [1,2,3,4,5]
# print(len(m))

# file1= open('C:/Users/Dunchuan/PycharmProjects/573proj01/DataSet/vectors/user-vectors-for-week-1.pkl', 'rb')
# data1 = pickle.load(file1)
# #data = {'Alice': 01s}
# for user, vector in data1.items():
#     binary_string1 = bin(vector)
