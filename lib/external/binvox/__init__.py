from subprocess import Popen , PIPE
from trimesh import Trimesh
from tempfile import mkdtemp
from .binvox_rw import read_as_3d_array
from numpy import ndarray, arange, array
from os.path import realpath, dirname

def sh(*args):
    popen = Popen(args, stdout=PIPE)
    popen.wait()
    return popen.stdout

def voxelize(mesh: Trimesh, dims:int = 14) -> ndarray:
    workdir = mkdtemp()
    TMP_FILE_NAME = workdir + '/voxelization'
    TMP_STL_FILE_NAME = TMP_FILE_NAME + '.stl'
    TMP_BINVOX_FILE_NAME = TMP_FILE_NAME + '.binvox'
    mesh.export(TMP_STL_FILE_NAME, 'stl')
    cmd_std = sh(dirname(realpath(__file__)) + "/binvox", '-d' , str(dims) , TMP_STL_FILE_NAME)
    vox_matrix = read_as_3d_array(open(TMP_BINVOX_FILE_NAME, 'rb'), fix_coords=True)
    return vox_matrix
