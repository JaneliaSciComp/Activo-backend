from kleio.stores import VersionedFSStore, ZarrIndexStore
import zarr


def create_kleio_dataset_reader(index_path, kv_path):
    try:
        index_store = ZarrIndexStore(index_path)
        store = VersionedFSStore(index_store, kv_path)
        return store
    except Exception as e:
        raise e
