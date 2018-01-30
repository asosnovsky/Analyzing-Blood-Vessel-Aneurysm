# Library
from base import S2_CLUSTERS_FILE, S2_CLUSTER_ALGO_FILE
from pandas import read_csv, DataFrame
from numpy import array, percentile
from tqdm import tqdm

# ARBITRARY CONSTANTS 
# need more work to figure optimal points, 
# at the moment these are manually set
MS_BANDWIDTH = 2.942783814571208
MAX_DISTANCE_QUANTILE = 85

# Start Loading Bar
pbar = tqdm(total=4)

# Read Data
centers_and_clusters:DataFrame = read_csv(S2_CLUSTERS_FILE)
cluster_labels:DataFrame = read_csv(S2_CLUSTER_ALGO_FILE)
pbar.update()

labels = cluster_labels.index

# Compute Distances
cx = centers_and_clusters['centroid_x']
cy = centers_and_clusters['centroid_y']
cz = centers_and_clusters['centroid_z']

msx = centers_and_clusters['ms_x']
msy = centers_and_clusters['ms_y']
msz = centers_and_clusters['ms_z']

pbar.update()

# Get Ready to plot
distances = DataFrame({
    'ms_dist': (((cx-msx)**2) + ((cy-msy)**2)  + ((cz-msz)**2))**0.5,
    'ms_middle': centers_and_clusters['ms_middle']
})
size = distances.groupby(['ms_middle'])['ms_dist'].max()

colors = array(['blue'] * len(size))
colors[size > percentile(size, q = MAX_DISTANCE_QUANTILE)] = 'red'

size = 1000*size/max(size)
pbar.update()

# Plot
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.pyplot import figure, show

fig = figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter( cluster_labels['x'], cluster_labels['y'], cluster_labels['z'], s=size, c=colors )

# from numpy import where

# cluster_ids = where( size > percentile(size, q = MAX_DISTANCE_QUANTILE) )[0].tolist()
# fileterd_set = centers_and_clusters.loc[[ms_mid in cluster_ids for ms_mid in distances['ms_middle']]]


# ax.scatter( 
#     fileterd_set['centroid_x'],
#     fileterd_set['centroid_y'],
#     fileterd_set['centroid_z'],
# )

# for cc_j in range(0,len(cluster_labels)):
#     ax.text( 
#         cluster_labels['x'][cc_j], 
#         cluster_labels['y'][cc_j], 
#         cluster_labels['z'][cc_j],  
#         str(cc_j), 
#         size=20, zorder=1, color='k'
#     ) 

pbar.update()
show()