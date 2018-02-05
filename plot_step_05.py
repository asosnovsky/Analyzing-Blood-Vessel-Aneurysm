# Library
from base import S5_CENTERS, S4_REDUCED_POINTS
from pandas import read_csv, DataFrame
from numpy import array
from tqdm import tqdm

# Read csv
centers:DataFrame = read_csv(S5_CENTERS)
reduce_triangles:DataFrame = read_csv(S4_REDUCED_POINTS)

# Plot
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.pyplot import figure, show

fig = figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter( 
    centers[['x']],
    centers[['y']],
    centers[['z']],
    c='green',
    s=50
)

ax.scatter( 
    reduce_triangles[['x']],
    reduce_triangles[['y']],
    reduce_triangles[['z']],
    c='blue',
    s=5
)

show()