from kleio.stores import VersionedFSStore, ZarrIndexStore
import zarr
from numcodecs import Zstd
from pathlib import Path
import numpy as np

# compressor = Zstd(level=1)
#
import shutil
import os

import kleio

path = '/Users/zouinkhim/Desktop/tmp/data_demo_versioned'
path_index = '/Users/zouinkhim/Desktop/tmp/index_demo_versioned'
if os.path.exists(path):
    shutil.rmtree(path)
if os.path.exists(path_index):
    shutil.rmtree(path_index)

index_store = ZarrIndexStore(path_index)
store = VersionedFSStore(index_store, path, auto_mkdir=True)
# TODO fix axes
z = zarr.open(store, mode="a")
z.create_dataset("test", shape=(1000, 1000, 10), chunks=(128, 128, 128), dtype= "u1")
x = z["test"]
# all = x[:]
# print("type: {}: ".format(type(z["test"])))
print("set dataset")
# x[:] = dummy_data
# x[[0, 0, 0], [0, 2, 3]] = 5

# x[0:60, :, 1:10] = 120
# x[100:300,:, 2:15] = 200

x[:, :, :] = 200

x[0:500, 0:400, :] = 50
# x[:, :, :] = 200

# x[0:60, 200:400, 1:10] = 120
# x[100:300, 100:150, 2:15] = 200
#
# x[500:900, 500:900, :] = 200
# x[6, 8] = 5
# print("read dataset")
# print(z["test"][:])
# z["test"][9, 0] = 20
# print(z["test"][0,0])
# root = zarr.group(store=store, overwrite=True)
# foo = root.create_group('foo')
# bar = foo.zeros('bar', shape=(10, 10), chunks=(5, 5), compressor=compressor)

# z = zarr.open(store=store, mode='w')
