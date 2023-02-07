import os

import shutil

import zarr
from kleio.stores import VersionedFSStore, N5FSIndexStore
from zarr.n5 import N5FSStore

from activo.data.convert import convert

path_n5 = '/Users/zouinkhim/Desktop/tmp/data/fly/dataset.n5'

path_kleio_indexes = '/Users/zouinkhim/Desktop/tmp/data/fly/kleio/indexes'
path_kleio_kv = '/Users/zouinkhim/Desktop/tmp/data/fly/kleio/kv'

if os.path.exists(path_kleio_indexes):
    shutil.rmtree(path_kleio_indexes)
if os.path.exists(path_kleio_kv):
    shutil.rmtree(path_kleio_kv)

store_n5 = N5FSStore(path_n5)
index_store = N5FSIndexStore(path_kleio_indexes)
store_kleio = VersionedFSStore(index_store, path_kleio_kv)

convert(zarr.open(store_n5), zarr.open(store_kleio))
