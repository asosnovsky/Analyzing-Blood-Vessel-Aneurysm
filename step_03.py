# Library
from base import S2_CLUSTERS_FILE, S2_CLUSTER_ALGO_FILE, S3_SELECTED_CLUSTERS
from pandas import read_csv, DataFrame
from numpy import array, percentile
from tqdm import tqdm

# ARBITRARY CONSTANTS 
# need more work to figure optimal points, 
# at the moment these are manually set
MAX_DISTANCE_QUANTILE = 85

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
# Calculate Sub Groups
# #############################################################################
chosen_groups = cluster_labels['ms_label'][size > percentile(size, q = MAX_DISTANCE_QUANTILE)].tolist()

chosen_groups = [11,24,15]
chosen_centers_and_clusters = centers_and_clusters.loc[[ j in chosen_groups for j in centers_and_clusters['ms_label'] ]]
pbar.update()

# #############################################################################
# Save
# #############################################################################
chosen_centers_and_clusters.to_csv(S3_SELECTED_CLUSTERS, index=False)
pbar.update()
