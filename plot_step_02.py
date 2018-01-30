# Library
from base import S2_CLUSTERS_FILE, S2_CLUSTER_ALGO_FILE
from pandas import read_csv, DataFrame
from numpy import array, percentile
from tqdm import tqdm

# ARBITRARY CONSTANTS 
# need more work to figure optimal points, 
# at the moment these are manually set
MAX_DISTANCE_QUANTILE = 80

# Start Loading Bar
pbar = tqdm(total=5)

# Read Data
centers_and_clusters:DataFrame = read_csv(S2_CLUSTERS_FILE)
cluster_labels:DataFrame = read_csv(S2_CLUSTER_ALGO_FILE)
pbar.update()

# #############################################################################
# Compute Distances
# #############################################################################
# Grab Vectors
cx = centers_and_clusters['centroid_x']
cy = centers_and_clusters['centroid_y']
cz = centers_and_clusters['centroid_z']

msx = centers_and_clusters['ms_x']
msy = centers_and_clusters['ms_y']
msz = centers_and_clusters['ms_z']

pbar.update()

# Calculate
distances = DataFrame({
    'ms_dist': (((cx-msx)**2) + ((cy-msy)**2)  + ((cz-msz)**2))**0.5,
    'ms_label': centers_and_clusters['ms_label']
})
size = distances.groupby(['ms_label'])['ms_dist'].max()
pbar.update()

# #############################################################################
# Plot
# #############################################################################
# Create Color Schemes
colors = array(['blue'] * len(size))
colors[size > percentile(size, q = MAX_DISTANCE_QUANTILE)] = 'red'

# Size it
size = 1000*size/max(size)
pbar.update()

# Plot
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.pyplot import figure, show

fig = figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter( 
    cluster_labels['x'],
    cluster_labels['y'],
    cluster_labels['z'],
    s=size, c=colors 
)
pbar.update()


for cc_j in range(0,len(cluster_labels)):
    ax.text( 
        cluster_labels['x'][cc_j], 
        cluster_labels['y'][cc_j], 
        cluster_labels['z'][cc_j],  
        str(cc_j), 
        size=20, zorder=1, color='k'
    ) 
pbar.update()

show()

