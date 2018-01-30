# Library
from base import S1_CENTERS_FILE, S2_CLUSTERS_FILE, S2_CLUSTER_ALGO_FILE
from pandas import read_csv, DataFrame
from tqdm import tqdm

# ARBITRARY CONSTANTS 
# need more work to figure optimal points, 
# at the moment these are manually set
MS_BANDWIDTH = 2.942783814571208
MAX_DISTANCE_QUANTILE = 85

# Start Loading Bar
pbar = tqdm(total=5)

# Read Data
triangles:DataFrame = read_csv(S1_CENTERS_FILE)
pbar.update()

# #############################################################################
# Algo
# #############################################################################
from sklearn.cluster import MeanShift, estimate_bandwidth
from numpy import percentile, array
from pandas import DataFrame, Series, merge

# Get Just the centers
triangle_centers = triangles[['centroid_x','centroid_y','centroid_z']].as_matrix()
pbar.update()

# clustering with MeanShift
ms = MeanShift(bandwidth=MS_BANDWIDTH, bin_seeding=True)
ms.fit(triangle_centers)
pbar.update()

# Grab Cluster Labels
triangles['ms_label'] = Series(ms.labels_, index=triangles.index)
pbar.update()

# Attach Cluster Centers
centers_and_clusters = triangles.merge( 
    DataFrame(ms.cluster_centers_, columns=['ms_x','ms_y','ms_z']), 
    left_on='ms_label', 
    right_index=True 
)

# Save
merge(
    DataFrame(ms.labels_, columns=['ms_label']),
    DataFrame(ms.cluster_centers_, columns=['x','y','z']),
    left_index=True, right_index=True
).to_csv(S2_CLUSTER_ALGO_FILE, index=False)
centers_and_clusters.to_csv(S2_CLUSTERS_FILE, index=False)
pbar.update()
