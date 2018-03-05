from pandas import read_csv

from mpl_toolkits.mplot3d import Axes3D
from matplotlib.pyplot import figure, show

fig = figure()
ax = fig.add_subplot(111, projection='3d')

for idx in range(0,len(skel_points_mesh)-1):
    ax.plot(
        skel_points_mesh[ [i + idx for i in range(0,2)] ,0],
        skel_points_mesh[ [i + idx for i in range(0,2)] ,1],
        skel_points_mesh[ [i + idx for i in range(0,2)] ,2],
    )

ax.scatter( 
    skel_points_mesh[:,0],
    skel_points_mesh[:,1],
    skel_points_mesh[:,2],
    c='green',
    s=50
)
show()



# from lib.base.constants.files import S0_VESSELS_FILE, S1_TRIANGLES_FILE
# from lib.base.constants.numbers import EPSLION
# from lib.s01_convert_stl import convert_stl_to_csv
# from lib.voxelize import load_voxel_from_mesh_file

# # Step 01
# # convert_stl_to_csv(S0_VESSELS_FILE, S1_TRIANGLES_FILE)

# # ??
# # from skimage.morphology import skeletonize_3d
# # from trimesh import load_mesh

# vox_mesh = load_voxel_from_mesh_file(S0_VESSELS_FILE, dims=100)

# # from tqdm import tqdm
# # from mpl_toolkits.mplot3d import Axes3D
# # from matplotlib.pyplot import figure, show

# # # vox_mesh.shape (31, 55, 77)

# # skel_vox_mesh = skeletonize_3d(vox_mesh)

# # fig = figure()
# # ax = fig.add_subplot(111, projection='3d')

# # max_x, max_y, max_z = vox_mesh.shape

# # for xi in tqdm(range(0, max_x)):
# #     for yi in tqdm(range(0, max_y)):
# #         for zi in tqdm(range(0,max_z)):
# #             # if vox_mesh[xi,yi,zi]:
# #             #     ax.scatter( 
# #             #         xi,
# #             #         yi,
# #             #         zi,
# #             #         color='green' 
# #             #     )
# #             if skel_vox_mesh[xi,yi,zi]:
# #                 ax.scatter( 
# #                     xi,
# #                     yi,
# #                     zi,
# #                     color='yellow' 
# #                 )
# #                 ax.scatter( 
# #                     [xi-1,xi+1],
# #                     [yi]*2,
# #                     [zi]*2,
# #                     color='red' 
# #                 )
# # show()