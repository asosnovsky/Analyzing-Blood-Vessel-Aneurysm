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

def voxelize(mesh: Trimesh, dims:int = 14):
    workdir = mkdtemp()
    # workdir = '/home/ari/projects/Analysis/blood_vessel_aneurysm'
    TMP_FILE_NAME = workdir + '/voxelization'
    TMP_STL_FILE_NAME = TMP_FILE_NAME + '.stl'
    TMP_BINVOX_FILE_NAME = TMP_FILE_NAME + '.binvox'
    mesh.export(TMP_STL_FILE_NAME, 'stl')
    cmd_std = sh(dirname(realpath(__file__)) + "/binvox", '-d' , str(dims) , TMP_STL_FILE_NAME)
    
    print("\n".join(map(lambda s: s.decode("utf-8"), cmd_std.readlines())))

    vox_matrix = read_as_3d_array(open(TMP_BINVOX_FILE_NAME, 'rb'), fix_coords=True)
    # sh('rm', '-rf', workdir)
    return vox_matrix

def make_mesh(norms: ndarray, vertices: ndarray) -> Trimesh:
    # Convert to Mesh coordinates
    faces = []
    verts = []

    for idx in range(0, len(norms)):
        norm_x, norm_y, norm_z = norms[idx]
        x1,y1,z1,x2,y2,z2,x3,y3,z3 = vertices[idx]
        faces += [ [norm_x,norm_y,norm_z] ]
        verts += [ 
            [x1,y1,z1],
            [x2,y2,z2],
            [x3,y3,z3]
        ]

    # Convert to Mesh 
    return Trimesh(
        vertices=array(verts),
        faces=arange(int(len(faces)*3)).reshape((-1, 3)),
        face_normals=array(faces)
    )