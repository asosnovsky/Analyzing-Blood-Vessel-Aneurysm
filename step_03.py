
# Libraries
from base import POINTS_DIR, LINES_FILE, delete_if_exists, Logger
from numpy import array, float, ndarray
from numpy import transpose as t, ones, identity
from numpy import argmin, argmax, amin
from numpy import where, delete
from math import inf
from tqdm import tqdm
from os import listdir
from pandas import read_csv, DataFrame

# logger
logger = Logger('step_03.log')

# some methods
class Center:
    def __init__(self, point):
        self.x = point[0]
        self.y = point[1]
        self.z = point[2]
    def __sub__(self, it) -> float:
        return ( (self.x - it.x)**2 + (self.y - it.y)**2 + (self.z - it.z)**2 ) ** 0.5

def calc_distances(points: ndarray) -> ndarray:
    A = array([
        Center(point) for point in points
    ])
    A = array(((A,))*len(A))
    B = t(A)
    return(A-B)

# Clear triangles that are too close to one another i.e. <1
def remove_too_close(distances:ndarray, epsilon:float=1):
    processed = []
    keep_us = []
    idx = 0
    while len(processed) < len(distances) and idx < len(distances):
        if idx not in processed:
            keep_us += [idx]
            if sum(distances[idx] < epsilon) > 1:
                to_remove = where(distances[idx] < epsilon)
                processed += to_remove[0].tolist()
            else:
                processed += [idx]
        idx+=1
    return(keep_us)

def get_lowest_idicies(m:ndarray) -> list:
    adj_m = m.copy()
    mask = identity(len(m))
    adj_m[mask==1] = inf
    return(argmin(adj_m, axis=1).tolist())

# Grouping Algo
def algo_when_odd_minimas(minimas:list) -> list:
    processed = []
    idx = 0
    minimas_cp = minimas.copy()
    while idx < len(minimas) and len(processed) < len(minimas):
        if idx not in processed:
            if minimas[minimas[idx]] == idx:            
                processed += [minimas[idx]]
            else:
                minimas_cp[idx] = idx
            processed += [idx]
        idx+=1
    return(minimas_cp)

def algo_when_even(distances:ndarray, minimas:list) -> list:
    arr_minimas = array(minimas)
    processed = []
    for minima in set(minimas):
        count = minimas.count(minima)
        if count > 1 and minima not in processed and minimas[minima] not in processed:
            closets_distances = distances[minima,where(arr_minimas==minima)]
            closets_distances_no_argmin = delete(closets_distances,argmin(closets_distances))
            my_real_minima = where(distances[minima,:] == min(closets_distances_no_argmin))[0][0]
            distances[ :, minima ] = inf
            distances[ minima, : ] = inf
            distances[ :, my_real_minima ] = inf
            distances[ my_real_minima, : ] = inf
            distances[ my_real_minima, minima ] = -inf
            distances[ minima, my_real_minima ] = -inf
            processed += [ minima, my_real_minima ]
    return(get_lowest_idicies(distances))

def algo_main_func(distances:ndarray) -> list:
    minimas = get_lowest_idicies(distances)
    set_minimas = set(minimas)
    if len(set_minimas) < len(minimas):
        if len(minimas) % 2 == 0:
            return(algo_when_even(distances.copy(), minimas))
        else:
            algo_when_odd_minimas(minimas)
    return(minimas)

# Write onto file
# grab all groupings
file_names = listdir(POINTS_DIR)
delete_if_exists(LINES_FILE)

# open output file
line_file = open(LINES_FILE, 'a')

# Write headers
line_file.writelines('line_idx,v1_triangle_idx,v2_triangle_idx,distance,v1_x,v1_y,v1_z,v2_x,v2_y,v2_z\n')

# Function for processing one file
def process_file(file_name: str):
    logger.log('Reading "{}"'.format(file_name))
    # read file
    points = read_csv(POINTS_DIR + file_name)
    
    # ignore empty files
    if len(points) == 0:
        return(0)

    logger.log('Calculating distances...')
    # Calculate Distances and clean them
    dists = calc_distances(
        points[['centroid_x','centroid_y','centroid_z']].as_matrix()
    )
    logger.log('Cleaning distances...')
    keep_us = remove_too_close(dists)
    points = points.loc[keep_us].reset_index()
    
    logger.log('Grouping by distances...')
    # Group centers by distances
    vectors = points[['centroid_x','centroid_y','centroid_z']].as_matrix()
    distances = calc_distances(vectors)
    minimas = algo_main_func(distances)

    logger.log('Saving...')
    # Save onto file
    saved = []
    line_idx = 0
    
    while len(saved) < len(minimas) and line_idx < len(minimas):
        if line_idx not in saved:
            logger.log('Saving...{}'.format(line_idx))
            v1_triangle_idx = int(points[['triangle_idx']].loc[line_idx])
            v2_triangle_idx = int(points[['triangle_idx']].loc[minimas[line_idx]])
            distance = distances[line_idx, minimas[line_idx]]
            v1,v2 = vectors[[line_idx, minimas[line_idx]]]
            if distance > 0:
                line_file.writelines(",".join(map(str,[
                    line_idx,
                    v1_triangle_idx, v2_triangle_idx,
                    distance
                ] + v1.tolist() + v2.tolist())) + '\n')
            saved += [line_idx, minimas[line_idx]]
        line_idx+=1

# main loop
for file_name in tqdm(file_names):
    process_file(file_name)
# process_file('45.csv')