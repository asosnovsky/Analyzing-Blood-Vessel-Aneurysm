# Analyzing Blood Vessel Aneurysm

This repository contains **only the code** used to extract positional data from the stl file provided.
The process is split up into 4 steps.

- Step 1: Parse the stl file, and reduce it to a csv
- Step 2: Identify centroids of triangle faces, and locate parrellel triangles
- Step 3: Subgroup the parrellel triangles in pairs, then compute: distance and center between the triangle's centroids
- Step 4: Use centroids and distance of triangles as the diameter and center of each cross-section of the vessel

## Notes
I was hoping to refine the identification of the cross-section, by re-grouping the pairs of triangles in Step 3. Additionally, there is no official statistical model in this example, as due to lack of time I was focusing on getting the data needed from the 3d-rendering.