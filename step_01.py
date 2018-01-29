
# Library
from base import S0_VESSELS_FILE, S1_CENTERS_FILE, delete_file_if_exists
from numpy import dot, array
from stl import mesh
from tqdm import tqdm

# Load data
data_mesh = mesh.Mesh.from_file(S0_VESSELS_FILE)

# Delete Data if exists
delete_file_if_exists(S1_CENTERS_FILE)

# Open File
with open(S1_CENTERS_FILE, 'a') as data_file:
    # Write Headers
    data_file.write('triangle_idx,centroid_x,centroid_y,centroid_z,norm_x,norm_y,norm_z\n')
    # Compute key variables
    for triangle_idx,vector in enumerate(tqdm(data_mesh.vectors)):
        data_file.write(",".join(map(str,
            [triangle_idx] + dot(array([1/3,1/3,1/3]),vector).tolist() + data_mesh.normals[triangle_idx].tolist()
        ))+'\n')
    