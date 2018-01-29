# Library
from base import S1_CENTERS_FILE
from pandas import read_csv, DataFrame
from tqdm import tqdm

# ARBITRARY CONSTANTS 
# need more work to figure optimal points, 
# at the moment these are manually set
MS_BANDWIDTH = 2.942783814571208
MAX_DISTANCE_QUANTILE = 85

# Start Loading Bar
pbar = tqdm(total=8)

# Read Data
triangles:DataFrame = read_csv(S1_CENTERS_FILE)
pbar.update()

# #############################################################################
# Algo
# #############################################################################
from sklearn.cluster import MeanShift, estimate_bandwidth
from numpy import percentile, array
from pandas import DataFrame, Series

# Get Just the centers
triangle_centers = triangles[['centroid_x','centroid_y','centroid_z']].as_matrix()
pbar.update()

# clustering with MeanShift
ms = MeanShift(bandwidth=MS_BANDWIDTH, bin_seeding=True)
ms.fit(triangle_centers)
pbar.update()

# Grab Cluster Labels
triangles['ms_middle'] = Series(ms.labels_, index=triangles.index)
pbar.update()

# Attach Cluster Centers
centers_and_clusters = triangles.merge( 
    DataFrame(ms.cluster_centers_, columns=['ms_x','ms_y','ms_z']), 
    left_on='ms_middle', 
    right_index=True 
)
centers_and_clusters.to_csv('centers_and_clusters.csv')
pbar.update()

# Compute Distances
cx = centers_and_clusters['centroid_x']
cy = centers_and_clusters['centroid_y']
cz = centers_and_clusters['centroid_z']

msx = centers_and_clusters['ms_x']
msy = centers_and_clusters['ms_y']
msz = centers_and_clusters['ms_z']

pbar.update()

# Get Ready to plot
size = DataFrame({
    'ms_dist': (((cx-msx)**2) + ((cy-msy)**2)  + ((cz-msz)**2))**0.5,
    'ms_middle': ms.labels_
}).groupby(['ms_middle'])['ms_dist'].max()

colors = array(['blue'] * len(size))
colors[size > percentile(size, q = MAX_DISTANCE_QUANTILE)] = 'red'

size = 1000*size/max(size)
pbar.update()

# Plot
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.pyplot import figure, show

fig = figure()
ax = fig.add_subplot(111, projection='3d')
# ax.scatter( ms.cluster_centers_[:,0], ms.cluster_centers_[:,1], ms.cluster_centers_[:,2], s=size, c=colors )
ax.scatter( 
    centers_and_clusters[:,0], 
    centers_and_clusters[:,1], 
    centers_and_clusters[:,2], 
    s=[ size[ms_middle] for ms_middle in centers_and_clusters['ms_middle'] ], 
    c=[ colors[ms_middle] for ms_middle in centers_and_clusters['ms_middle'] ], 
)

for cc_j in range(0,len(ms.cluster_centers_)):
    ax.text( 
        ms.cluster_centers_[cc_j,0], 
        ms.cluster_centers_[cc_j,1], 
        ms.cluster_centers_[cc_j,2],  
        str(cc_j), 
        size=20, zorder=1, color='k'
    ) 

pbar.update()
show()