"""
    This file is where the final algo will take place
    At the moment, I only look at the values that are above a given quantile
    Ideally, we would want to run a more robust model
"""

# Libraries
from base import LINES_FILE, CENTROIDS_FILE, delete_if_exists, Logger, plot3d
from numpy import array, float, ndarray
from tqdm import tqdm
from pandas import read_csv, DataFrame

# General Methods
def angle_between(v1_u:ndarray, v2_u:ndarray) -> float:
    """ Returns the angle in radians between vectors 'v1' and 'v2'::
    """
    from numpy import arccos, clip, dot
    return arccos(clip(dot(v1_u, v2_u), -1.0, 1.0))

# Read Lines File
lines_data:DataFrame = read_csv(LINES_FILE)

sorted_data:DataFrame = lines_data[['center_x','center_y','center_z','distance']].sort_values(['distance'])

low_end = sorted_data['distance'].quantile(0.9)
filtered_data:DataFrame = sorted_data[ sorted_data['distance'] > low_end ]


# Save
filtered_data[['center_x','center_y','center_z']].to_csv(CENTROIDS_FILE)

# Plot
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

m = sorted_data.as_matrix()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter( 
    m[:,0].tolist(), 
    m[:,1].tolist(), 
    m[:,2].tolist(), 
    c='b',
    # linewidths=(m[:,3]).tolist()
)
plt.show()

