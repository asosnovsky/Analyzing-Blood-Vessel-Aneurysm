# Library
from base import S1_CENTERS_FILE
from pandas import read_csv, DataFrame
from tqdm import tqdm

pbar = tqdm(total=8)

# Constants
MS_BANDWIDTH = 2.942783814571208
MAX_DISTANCE_QUANTILE = 85

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

# clustering with MeanShift
ms = MeanShift(bandwidth=MS_BANDWIDTH, bin_seeding=True)
ms.fit(triangle_centers)
pbar.update()

# Grab Cluster Labels
triangles['ms_middle'] = Series(ms.labels_, index=triangles.index)

# Attach Cluster Centers
centers_and_clusters = triangles.merge( 
    DataFrame(ms.cluster_centers_, columns=['ms_x','ms_y','ms_z']), 
    left_on='ms_middle', 
    right_index=True 
)
pbar.update()


# #############################################################################
# Compute Distances
# #############################################################################
cx = centers_and_clusters['centroid_x']
cy = centers_and_clusters['centroid_y']
cz = centers_and_clusters['centroid_z']

msx = centers_and_clusters['ms_x']
msy = centers_and_clusters['ms_y']
msz = centers_and_clusters['ms_z']

# Get Ready to plot
distances = DataFrame({
    'ms_dist': (((cx-msx)**2) + ((cy-msy)**2)  + ((cz-msz)**2))**0.5,
    'ms_middle': centers_and_clusters['ms_middle']
})
size = distances.groupby(['ms_middle'])['ms_dist'].max()
pbar.update()

colors = array(['blue'] * len(size))
colors[size > percentile(size, q = MAX_DISTANCE_QUANTILE)] = 'red'

size = 1000*size/max(size)
pbar.update()


# #############################################################################
# Plot
# #############################################################################
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.pyplot import figure, show

fig = figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter( ms.cluster_centers_[:,0], ms.cluster_centers_[:,1], ms.cluster_centers_[:,2], s=size, c=colors )
pbar.update()

show()