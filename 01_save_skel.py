from lib.base.constants.files import S0_VESSELS_FILE, S1_SKEL_FILE
from lib.base.constants.numbers import EPSLION
from trimesh import load_mesh
from lib.external.binvox import voxelize
from pandas import DataFrame

mesh = load_mesh(S0_VESSELS_FILE)
voxed_mesh = voxelize(mesh, dims=56)

from skimage.morphology import skeletonize_3d
from trimesh.voxel import matrix_to_points

skel_voxed_mesh = skeletonize_3d(voxed_mesh.data)
skel_points_mesh = matrix_to_points(skel_voxed_mesh, pitch=1, origin=[0,0,0])

DataFrame(
    skel_points_mesh, 
    columns=['x','y','z']
).to_csv(
    S1_SKEL_FILE,
    index=False
)