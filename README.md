# Analyzing Blood Vessel Aneurysm

This repository contains **only the code** used to extract positional data from the stl file provided.
The process is split up into 4 steps.

- Step 1: Parse the stl file, and reduce it to a csv
- Step 2: Use Mean Shift clustering to identify various groupings in data
- Step 3: List groupings that contain high diameters, then choose visually the correct cluster
- Step 4: Use mean-shift to lower the resolution of the selected grouping


## How to use
Extract `vessels.stl.zip` into `data/` as `data/00_vessel.stl`.
Then run (in order)

```
    python step_01.py
    python step_02.py
    python step_03.py
    python step_04.py
```
