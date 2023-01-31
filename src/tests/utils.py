from kleio.stores import VersionedFSStore, ZarrIndexStore
import zarr


def create_kleio(index_path, kv_path, dataset):
    index_store = ZarrIndexStore(index_path)
    store = VersionedFSStore(index_store, kv_path)
    z = zarr.open(store, mode="a")
    z.create_dataset(dataset, shape=(1000, 1000, 10), chunks=(128, 128, 128), dtype="u1")
