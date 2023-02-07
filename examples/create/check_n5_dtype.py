import json
# import zarr
from zarr.n5 import N5FSStore
from zarr.storage import MemoryStore
import shutil
import os
from zarr.creation import create

path_n5 = '/Users/zouinkhim/Desktop/tmp/test_n5.n5'

if os.path.exists(path_n5):
    shutil.rmtree(path_n5)

# n5_store = N5FSStore(path_n5)
# z = create(100, store=n5_store)
#
# print(json.loads(create(100).store[".zarray"]))
# print(json.loads(n5_store[".zarray"]))
# '/Users/zouinkhim/Desktop/tmp/test_n5.n5'


# path = 'data/array.n5'
# atexit.register(atexit_rmtree, path)
n5_store = N5FSStore(path_n5)
create(100, store=n5_store)
dtype_n5 = json.loads(n5_store[".zarray"])["dtype"]
dtype_zarr = json.loads(create(100).store[".zarray"])["dtype"]

print(dtype_n5)
print(dtype_zarr)