# Library
from base import S2_SUB_GROUPS_FOLDER, S3_SUB_GROUPS_LINES_FOLDER, FileSaver, create_clean_folder, is_parrelel
from numpy import array, ndarray
from pandas import read_csv, DataFrame
from tqdm import tqdm
from os import listdir
from multiprocessing.dummy import Pool as ThreadPool 
from re import sub as strsub

# Read Files
groupings_files = listdir(S2_SUB_GROUPS_FOLDER)

# Methods
def grab_norm(dt:DataFrame, idx:int) -> ndarray:
    return(array([
        dt.loc[idx]['norm_x'],
        dt.loc[idx]['norm_y'],
        dt.loc[idx]['norm_z'],
    ]))

def find_all_parrellels(dt:DataFrame, idx: int) -> DataFrame:
    parrellels = {
        'triangle_idx': [],
        'theta': [],
    }
    min_theta = 1000000
    my_norm = grab_norm(dt, idx)

    def run_once(i: int):
        if i != idx:
            their_norm = grab_norm(dt, i)
            isparrellel, theta = is_parrelel(my_norm, their_norm, epsilon=0.01)
            if isparrellel:
                parrellels['triangle_idx'] += [int(dt.loc[i]['triangle_idx'])]
                parrellels['theta'] += [theta]

    pool = ThreadPool(4) 
    results = pool.map(run_once, range(0, len(dt)-1))
    if len(parrellels['theta']) > 0:
        parrellels['target_idx'] = [idx]*len(parrellels['theta'])
        return DataFrame(parrellels)
    else:
        return None
            

# Reset main save folder
create_clean_folder(S3_SUB_GROUPS_LINES_FOLDER)


grouping_file:str = groupings_files[1]

# Create Save Folder
SAVE_FOLDER = S3_SUB_GROUPS_LINES_FOLDER + strsub('\.csv$', '', grouping_file) + '/'
create_clean_folder(SAVE_FOLDER)

# Read Data
centers:DataFrame = read_csv(S2_SUB_GROUPS_FOLDER + grouping_file)

# Run Loop
processed = []
idx = 0
pbar = tqdm(total=len(centers))
while idx < len(centers) and len(processed) < len(centers):
    if idx not in processed:
        processed += [idx]
        abs_parrellel = find_all_parrellels(centers, idx)
        if abs_parrellel is not None:
            abs_parrellel.to_csv(SAVE_FOLDER + str(idx) + '.csv', index=False)
            processed += abs_parrellel['target_idx'].as_matrix().tolist()

    pbar.update(len(processed)-pbar.n)
    idx+=1


