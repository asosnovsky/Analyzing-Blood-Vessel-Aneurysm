
# Library
from base import S0_VESSELS_FILE, S1_TRIANGLES_FILE, FileSaver
from numpy import dot, array
from stl import mesh
from tqdm import tqdm

# Load data
data_mesh = mesh.Mesh.from_file(S0_VESSELS_FILE)

# Open File
triangles = FileSaver(S1_TRIANGLES_FILE)

# Write Headers
triangles.write('triangle_idx,centroid_x,centroid_y,centroid_z,norm_x,norm_y,norm_z,x1,y1,z1,x2,y2,z2,x3,y3,z3')

# Compute key variables
for triangle_idx,vector in enumerate(tqdm(data_mesh.vectors)):
    triangles.write(",".join(map(str,
        [triangle_idx] + 
        dot(array([1/3,1/3,1/3]),vector).tolist() + 
        data_mesh.normals[triangle_idx].tolist()
    )) + "," + ",".join(map( lambda s: ",".join(map(str, s)) , vector.tolist())))

    