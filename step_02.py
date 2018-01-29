
# Library
from base import S1_CENTERS_FILE, S2_SUB_GROUPS_FOLDER, delete_file_if_exists, create_clean_folder
from numpy import array, ndarray
from pandas import read_csv, DataFrame
from tqdm import tqdm

# Progress
pbar = tqdm(total=14)

# Read Data
centers:DataFrame = read_csv(S1_CENTERS_FILE)

pbar.update()
# 5-Number Summary
number_summary = centers.describe()

split_point = array([
    number_summary['centroid_x']['50%'], 
    number_summary['centroid_y']['50%'], 
    number_summary['centroid_z']['50%']
])

def split_by_point(dt:DataFrame, axis, num) -> (DataFrame, DataFrame):
    return( 
        dt[ dt[[axis]].as_matrix() > num ],
        dt[ dt[[axis]].as_matrix() <= num ]
    )

pbar.update()
# Split by X-axis
grp_X_top, grp_X_bottom = split_by_point(centers, 'centroid_x', split_point[0])
pbar.update()

# Split by Y-axis
grp_X_top_Y_top, grp_X_top_Y_bottom = split_by_point(grp_X_top, 'centroid_y', split_point[1])
grp_X_bottom_Y_top, grp_X_bottom_Y_bottom = split_by_point(grp_X_bottom, 'centroid_y', split_point[1])
pbar.update()

# Split by Z-axis
grp_X_top_Y_top_Z_top, grp_X_top_Y_top_Z_bottom = split_by_point(grp_X_top_Y_top, 'centroid_z', split_point[2])
grp_X_top_Y_bottom_Z_top, grp_X_top_Y_bottom_Z_bottom = split_by_point(grp_X_top_Y_bottom, 'centroid_z', split_point[2])

grp_X_bottom_Y_top_Z_top, grp_X_bottom_Y_top_Z_bottom = split_by_point(grp_X_bottom_Y_top, 'centroid_z', split_point[2])
grp_X_bottom_Y_bottom_Z_top, grp_X_bottom_Y_bottom_Z_bottom = split_by_point(grp_X_bottom_Y_bottom, 'centroid_z', split_point[2])
pbar.update()

# Save
create_clean_folder(S2_SUB_GROUPS_FOLDER);pbar.update()

grp_X_top_Y_top_Z_top.to_csv(S2_SUB_GROUPS_FOLDER + 'grp_X_top_Y_top_Z_top.csv', index=False);pbar.update()
grp_X_top_Y_top_Z_bottom.to_csv(S2_SUB_GROUPS_FOLDER + 'grp_X_top_Y_top_Z_bottom.csv', index=False);pbar.update()
grp_X_top_Y_bottom_Z_top.to_csv(S2_SUB_GROUPS_FOLDER + 'grp_X_top_Y_bottom_Z_top.csv', index=False);pbar.update()
grp_X_top_Y_bottom_Z_bottom.to_csv(S2_SUB_GROUPS_FOLDER + 'grp_X_top_Y_bottom_Z_bottom.csv', index=False);pbar.update()
grp_X_bottom_Y_top_Z_top.to_csv(S2_SUB_GROUPS_FOLDER + 'grp_X_bottom_Y_top_Z_top.csv', index=False);pbar.update()
grp_X_bottom_Y_top_Z_bottom.to_csv(S2_SUB_GROUPS_FOLDER + 'grp_X_bottom_Y_top_Z_bottom.csv', index=False);pbar.update()
grp_X_bottom_Y_bottom_Z_top.to_csv(S2_SUB_GROUPS_FOLDER + 'grp_X_bottom_Y_bottom_Z_top.csv', index=False);pbar.update()
grp_X_bottom_Y_bottom_Z_bottom.to_csv(S2_SUB_GROUPS_FOLDER + 'grp_X_bottom_Y_bottom_Z_bottom.csv', index=False);pbar.update()


