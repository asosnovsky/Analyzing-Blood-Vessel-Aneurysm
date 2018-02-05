
# Library
from base import S3_SELECTED_CLUSTERS, S4_REDUCED_POINTS
from lib import voxelize, make_mesh
from trimesh.voxel import matrix_to_points
from skimage.morphology import skeletonize_3d
from pandas import read_csv, DataFrame
from numpy import array
from tqdm import tqdm

# Read csv
selected_clusters:DataFrame = read_csv(S3_SELECTED_CLUSTERS)
reduce_triangles:DataFrame = read_csv(S4_REDUCED_POINTS)


mesh = make_mesh(
    selected_clusters[['norm_x','norm_y','norm_z']].as_matrix(), 
    selected_clusters[['x1','y1','z1','x2','y2','z2','x3','y3','z3']].as_matrix()
)
voxed_mesh = mesh.voxelized(1)
binvox_mesh = voxelize(mesh, 50)
# sam = skeletonize_3d(voxelize(mesh, 256).data)
voxed_coords_points = matrix_to_points(voxed_mesh.matrix, origin=voxed_mesh.origin, pitch=voxed_mesh.pitch)
binvox_coords_points = matrix_to_points(skeletonize_3d(binvox_mesh.data), origin=voxed_mesh.origin, pitch=voxed_mesh.pitch)

# Plot
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.pyplot import figure, show

fig = figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter( 
    binvox_coords_points[:,0],
    binvox_coords_points[:,1],
    binvox_coords_points[:,2],
    c='green',
    s=10
)
# ax.scatter( 
#     voxed_coords_points[:,0],#z
#     voxed_coords_points[:,1],#x
#     voxed_coords_points[:,2],#y
#     c='blue',
#     s=1
# )

ax.scatter( 
    reduce_triangles[['x']],
    reduce_triangles[['y']],
    reduce_triangles[['z']],
    c='blue',
    s=1
)



show()