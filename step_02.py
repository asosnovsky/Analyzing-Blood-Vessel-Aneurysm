
# Libraries
import base
from numpy import ndarray, array, float, linalg, clip, dot, arccos, pi, abs, concatenate
from tqdm import tqdm

# General Methods
def unit_vector(vector: ndarray):
    """ Returns the unit vector of the vector.  """
    return vector / linalg.norm(vector)

def angle_between(v1:ndarray, v2:ndarray) -> float:
    """ Returns the angle in radians between vectors 'v1' and 'v2'::
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return arccos(clip(dot(v1_u, v2_u), -1.0, 1.0))

def distance_vect(v1:ndarray, v2:ndarray) -> float:
    return( dot(array([1,1,1]),(v2-v1)**2)**0.5 )

def get_info_from_str(s: str) -> ndarray:
    triangle_idx,p1_x,p1_y,p1_z,p2_x,p2_y,p2_z,p3_x,p3_y,p3_z,norm_x,norm_y,norm_z,centroid_x,centroid_y,centroid_z = s.split(',')
    return(
        array([norm_x,norm_y,norm_z]).astype(float),
        array([centroid_x,centroid_y,centroid_z]).astype(float)
    )

def compare_norms(a:ndarray, b:ndarray, epsilon:float = base.EPSLION):
    theta = angle_between(a,b)
    return (theta < epsilon) or (abs(theta - pi) < epsilon), theta

# Create folder
base.create_clean_folder(base.POINTS_DIR)

# Finds a parrellel line group for a given triangle
def find_parrellel_line(origin_idx: int, ignore_list = [ 0 ]):
    origin_norm, origin_center = get_info_from_str(base.get_line_in_file(base.TRIANGLE_PROPS, origin_idx))
    output_ignore_list = ignore_list.copy()
    max_idx = 0
    # Open/Reset Output File
    base.delete_if_exists(base.POINTS_FILE % str(origin_idx))
    with open(base.POINTS_FILE % str(origin_idx), 'a') as points_file:
        # Write headers
        points_file.writelines('triangle_idx,parrellel_group_idx,centroid_x,centroid_y,centroid_z,angle,distance\n')
        with open(base.TRIANGLE_PROPS) as triangle_file:
            for compare_idx, line  in enumerate(triangle_file):
                if compare_idx not in ignore_list:
                    to_compare_norm, to_compare_center = get_info_from_str(line)
                    max_idx = compare_idx
                    is_parrellel, theta = compare_norms(origin_norm, to_compare_norm, 0.01)
                    if is_parrellel:
                        output_ignore_list += [compare_idx]
                        points_file.writelines(",".join(map(str,concatenate((
                            [compare_idx, origin_idx], 
                            to_compare_center, 
                            [theta, distance_vect(origin_center, to_compare_center)]
                        ))))+'\n')
    return(output_ignore_list, max_idx)
                
# Find parrellel group for first triangle
ignore_list = [ 0 ]
ignore_list, max_idx = find_parrellel_line(1, ignore_list)

# Find parrellel group for all
with tqdm(total=max_idx) as pbar:
    idx = 2
    while len(ignore_list) < max_idx and idx < max_idx:
        ignore_list, _ = find_parrellel_line(idx, ignore_list)
        pbar.update(len(ignore_list))
        idx+=1

