import K_means as km
import pandas as pd

sample_filename = "nmf-for-week-1.pkl"

#get the data points in each cluster
clusters_of_coordinates = km.get_cluster_stat(sample_filename)

# To find the correlation among the columns using pearson method
# StackOverflow: When the correlation coefficient is calculated, you divide by the standard deviation, which leads to a NA.
df = pd.DataFrame(clusters_of_coordinates[3])
coor_matrix = df.corr(method ='pearson')
print(coor_matrix)
