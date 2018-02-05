# Library
from base import S3_SELECTED_CLUSTERS, S5_CENTERS
from lib import voxelize, make_mesh
from trimesh.voxel import matrix_to_points
from skimage.morphology import skeletonize_3d
from pandas import read_csv, DataFrame
from numpy import array
from tqdm import tqdm

# Read csv
selected_clusters:DataFrame = read_csv(S3_SELECTED_CLUSTERS)

mesh = make_mesh(
    selected_clusters[['norm_x','norm_y','norm_z']].as_matrix(), 
    selected_clusters[['x1','y1','z1','x2','y2','z2','x3','y3','z3']].as_matrix()
)
voxed_mesh = mesh.voxelized(1)
binvox_mesh = voxelize(mesh, 20)

binvox_coords_points = matrix_to_points(skeletonize_3d(binvox_mesh.data), origin=voxed_mesh.origin, pitch=voxed_mesh.pitch)

DataFrame(
    binvox_coords_points, 
    columns=['x','y','z']
).to_csv(S5_CENTERS, index=False)