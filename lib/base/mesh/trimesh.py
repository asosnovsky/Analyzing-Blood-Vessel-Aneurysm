from trimesh import Trimesh
from numpy import ndarray, array

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