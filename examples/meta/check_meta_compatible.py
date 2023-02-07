# from kleio.stores import VersionedFSStore, ZarrIndexStore
# import zarr
# from numcodecs import Zstd
# from pathlib import Path
# import numpy as np
# from zarr.util import normalize_dtype
# # compressor = Zstd(level=1)
# #
# import shutil
# import os
# from zarr.n5 import N5FSStore
# import kleio
# from zarr.storage import FSStore
# import json
# path = '/Users/zouinkhim/Desktop/tmp/data_demo_versioned'
# path_index = '/Users/zouinkhim/Desktop/tmp/index_demo_versioned'
#
# # index_store = ZarrIndexStore(path_index)
# # store = VersionedFSStore(index_store, path)
# store = FSStore(path)
# # print(store["test/.zarray"])
#
# # z = zarr.open(store)
#
# # print(z["test"].shape)
# #
# # # print(normalize_dtype("|u1", object_codec=None))
# # x, _ = normalize_dtype("uint8", object_codec=None)
# # print(x.str)
# # n5 = N5FSStore(path)
# # z = zarr.open(n5)
#
# # print(z["test"].shape)
# array_metadata = json.loads(store["test/attributes.json"].decode())
# array_metadata['dimensions'] = array_metadata['dimensions'][::-1]
# array_metadata['blockSize'] = array_metadata['blockSize'][::-1]
# print(array_metadata)
# print()
#
#


