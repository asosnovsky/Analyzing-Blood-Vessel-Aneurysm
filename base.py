
# Files

## Step 00
S0_VESSELS_FILE = './data/00_vessel.stl'

## Step 01
S1_TRIANGLES_FILE = './data/01_triangles.csv'

## Step 02
S2_CLUSTERS_FILE = './data/02_centers_and_clusters.csv'
S2_CLUSTER_ALGO_FILE = './data/02_cluster.csv'

## Step 03
S3_SELECTED_CLUSTERS = './data/03_selected_centers_and_clusters.csv'

## Step 04
S4_REDUCED_POINTS = './data/04_reduced_points.csv'

## Step 05
S5_CENTERS = './data/05_centers.csv'

# Constants
EPSLION = 1E-4

# Methods - system
def delete_file_if_exists(filename: str):
    from os import remove
    try:
        remove(filename)
    except OSError:
        pass

def create_clean_folder(foldername: str):
    from os import path, makedirs
    from shutil import rmtree
    if path.exists(foldername):
        rmtree(foldername)
    makedirs(foldername)

class FileSaver:
    def __init__(self, file_name:str):
        delete_file_if_exists(file_name)
        self.__file_name = file_name
    def write(self, message:str, ext:str='\n'):
        f = open(self.__file_name, 'a')
        f.writelines(message + ext)
        f.close()
        
from subprocess import Popen , PIPE
def sh(*args, quiet:bool=True):
    popen = Popen(args, stdout=PIPE)
    popen.wait()
    if not quiet:
        print(popen.stdout.read())

# Methods - Plot
def plot3d(xs:list, ys:list, zs:list):
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib.pyplot import figure, show

    fig = figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter( xs, ys, zs )
    show()


# Methods - Calc
from numpy import ndarray
from numpy import pi, abs
from numpy import arccos, clip, dot
from numpy.linalg import norm

def unit_vector(vector: ndarray) -> ndarray:
    """ Returns the unit vector of the vector.  """
    return vector / norm(vector)

def angle_between(v1:ndarray, v2:ndarray) -> float:
    """ Returns the angle in radians between vectors 'v1' and 'v2'::
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return arccos(clip(dot(v1_u, v2_u), -1.0, 1.0))

def check_parallel(a:ndarray, b:ndarray, epsilon:float = EPSLION) -> (bool, float):
    """Determines if two lines are parallel, return bool, and angle
    """
    theta = angle_between(a,b)
    return (theta < epsilon) or (abs(theta - pi) < epsilon), theta
