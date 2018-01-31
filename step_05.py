# Library
from base import S4_REDUCED_POINTS, S5_CENTERS, FileSaver, check_parallel
from pandas import read_csv, DataFrame
from numpy import array
from tqdm import tqdm

# Read csv
reduced_clusters:DataFrame = read_csv(S4_REDUCED_POINTS)

# Create Save File
save_file = FileSaver(S5_CENTERS)
save_file.write('x,y,z,distance')

# Setup loop
MAX_LOOP = len(reduced_clusters)
pbar = tqdm(total= (MAX_LOOP+1)*(MAX_LOOP+1) )

# Run Loop
# idx = 5
for idx in range(0, MAX_LOOP):
    vect_0 = reduced_clusters.loc[idx]
    for comp_idx in range(0, MAX_LOOP):
        if comp_idx != idx:
            vect_1 = reduced_clusters.loc[comp_idx]
            is_parallel, theta = check_parallel(vect_1, vect_0, 0.01)
            if is_parallel:
                save_file.write(",".join(map(str, 
                    ( (vect_0+vect_1)/2 ).tolist() + [
                        sum( (vect_0-vect_1)**2 )**0.5
                    ]
                )))
        pbar.update()

pbar.close()