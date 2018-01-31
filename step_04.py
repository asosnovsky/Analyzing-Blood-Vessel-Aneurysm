# Library
from base import S3_SELECTED_CLUSTERS, S4_REDUCED_POINTS
from pandas import read_csv, DataFrame
from numpy import array, percentile
from tqdm import tqdm

pbar = tqdm(total=3)

# Read csv
clusters_and_centers:DataFrame = read_csv(S3_SELECTED_CLUSTERS)
pbar.update()

# Reduce numbers via clustering
from sklearn.cluster import MeanShift
ms = MeanShift(bandwidth=0.5, bin_seeding=True)
ms.fit(
    clusters_and_centers[['centroid_x','centroid_y','centroid_z']].as_matrix()
)
pbar.update()

# Save
DataFrame(
    ms.cluster_centers_,
    columns=['x','y','z']
).to_csv(S4_REDUCED_POINTS, index=False)
pbar.update()
