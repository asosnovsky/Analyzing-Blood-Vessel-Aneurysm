
# Files 

## Input
RAW_DATA = './data/00_vessel.stl'

## Step 01
TRIANGLE_PROPS = './data/01_triangles.csv'

## Step 02
POINTS_DIR = './data/02_points/'
POINTS_FILE = './data/02_points/%s.csv'

## Step 03
LINES_FILE = './data/03_lines.csv'

## Step 04
CENTROIDS_FILE = './data/04_upper_centroids.csv'


# Constants
EPSLION = 1E-4


# Utils
def delete_if_exists(filename: str):
    import os
    try:
        os.remove(filename)
    except OSError:
        pass

def create_clean_folder(foldername: str):
    from os import path, makedirs
    from shutil import rmtree
    if path.exists(foldername):
        rmtree(foldername)
    makedirs(foldername)

def get_line_in_file(filename: str, line_idx:int) -> str:
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            if i == line_idx:
                return line

from numpy import ndarray, ones
def remove_from_ndarray(arr:ndarray, idx:int) -> ndarray:
    mask = ones(len(arr))
    mask[idx] = 0
    return(arr[mask==1])

def plot3d(xs:list, ys:list, zs:list):
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    import numpy as np

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter( xs, ys, zs )
    print()
    print([xs, ys, zs])
    plt.show()

class Logger:
    def __init__(self, file_name:str):
        delete_if_exists(file_name)
        self.__file_name = file_name
    def log(self, message:str):
        f = open(self.__file_name, 'a')
        f.writelines(message + '\n')
        f.close()
