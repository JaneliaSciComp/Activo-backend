import zarr

import shutil
import os

path_zarr = '/Users/zouinkhim/Desktop/tmp/zarr'
if os.path.exists(path_zarr):
    shutil.rmtree(path_zarr)

z = zarr.open(path_zarr, mode="a")
z.create_dataset("test", shape=(1000, 1000, 30), chunks=(128, 128, 1), dtype="u1")
x = z["test"]

x[0:60, 200:400, 1:10] = 120
x[100:300, 100:150, 2:15] = 200

x[500:900, 500:900, :] = 200
