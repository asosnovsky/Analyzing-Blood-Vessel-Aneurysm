
# Libraries
import base
from numpy import array, dot, concatenate, savetxt
from stl import mesh
from tqdm import tqdm

# Load data
data_mesh = mesh.Mesh.from_file(base.RAW_DATA)

# Delete Data if exists
base.delete_if_exists(base.TRIANGLE_PROPS)

# Open File
with open(base.TRIANGLE_PROPS, 'a') as data_file:
    # Write Headers
    data_file.write('triangle_idx,p1_x,p1_y,p1_z,p2_x,p2_y,p2_z,p3_x,p3_y,p3_z,norm_x,norm_y,norm_z,centroid_x,centroid_y,centroid_z\n')
    # Compute key variables
    for triangle_idx,vector in enumerate(tqdm(data_mesh.vectors)):
        p1,p2,p3 = vector
        data_file.write(",".join(map(str,concatenate(
            ([triangle_idx], p1, p2, p3 , data_mesh.normals[triangle_idx] , dot(array([1/3,1/3,1/3]),vector))
        )))+'\n')
    