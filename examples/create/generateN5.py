import zarr

import shutil
import os

from zarr.n5 import N5FSStore

path_n5 = '/Users/zouinkhim/Desktop/tmp/n5'
if os.path.exists(path_n5):
    shutil.rmtree(path_n5)

store = N5FSStore(path_n5)

z = zarr.open(store, mode="a")
z.create_dataset("test", shape=(1000, 100, 30), chunks=(128, 128, 1), dtype= "u1")
x = z["test"]

x[0:60, :, 1:10] = 120
x[100:300,:, 2:15] = 200

x[500:900, :, :] = 200

