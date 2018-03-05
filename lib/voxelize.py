from skimage.morphology import skeletonize_3d
from trimesh import load_mesh
from .external.binvox import voxelize as binvox_voxelized
from .base.constants.files import VOXELIZATION_DIR
from .base.sys import create_clean_folder, path_leaf, FileSaver, path
from numpy import save as np_save, load as np_load

def load_voxel_from_mesh_file(mesh_path:str, dims:int = 56):
    create_clean_folder(VOXELIZATION_DIR, True)
    print(mesh_path)
    print(VOXELIZATION_DIR)
    file_path = VOXELIZATION_DIR + path_leaf(mesh_path).replace() + 'dims_' + str(dims) + '.npy'
    print(file_path)
    # if path.exists(file_path):
    #     return np_load(file_path)
    # else:
    #     mesh = load_mesh(mesh_path)
    #     vox_mesh = voxelize(mesh, dims=dims)
    #     np_save(file_path, vox_mesh.data)
    #     return vox_mesh.data