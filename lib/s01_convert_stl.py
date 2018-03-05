
# Library
from .base.sys import FileSaver
from numpy import dot, array
from stl import mesh
from tqdm import tqdm

def convert_stl_to_csv(stl_file_path:str, output_file_path:str, start_clean:bool = False):
    # Load data
    data_mesh = mesh.Mesh.from_file(stl_file_path)

    # Open File
    triangles = FileSaver(output_file_path, start_clean)

    # Write Headers
    if triangles.row_marker == 0:
        triangles.write('triangle_idx,centroid_x,centroid_y,centroid_z,norm_x,norm_y,norm_z,x1,y1,z1,x2,y2,z2,x3,y3,z3')

    # Count Vectors
    MAX_VECTORS = len(data_mesh.vectors)
    start_point = max(0, triangles.row_marker - 1)

    # Compute key variables
    for triangle_idx in tqdm(range(start_point, MAX_VECTORS), desc="> Converting STL to CSV..."):
        vector = data_mesh.vectors[triangle_idx]
        triangles.write(",".join(map(str,
            [triangle_idx] + 
            dot(array([1/3,1/3,1/3]),vector).tolist() + 
            data_mesh.normals[triangle_idx].tolist()
        )) + "," + ",".join(map( lambda s: ",".join(map(str, s)) , vector.tolist())))

        