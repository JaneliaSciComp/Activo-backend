from kleio.stores import VersionedFSStore, ZarrIndexStore
from starlette.responses import Response


def create_kleio_dataset_reader(index_path, kv_path):
    try:
        index_store = ZarrIndexStore(index_path)
        store = VersionedFSStore(index_store, kv_path)
        return store
    except Exception as e:
        raise e


def format_array_meta_fix_n5(array_metadata):
    array_metadata['dimensions'] = array_metadata['dimensions'][::-1]
    array_metadata['blockSize'] = array_metadata['blockSize'][::-1]
    return array_metadata
    # return Response(bytes(array_metadata, 'utf-8'), media_type='binary/octet-stream')


def format_chunk_n5_to_zarr_key(path):
    elms = path.split("/")
    path_parts = []
    axes = []
    for elm in elms:
        if str(elm).isdigit():
            axes.append(elm)
        else:
            path_parts.append(elm)
    #   hack to invert axes between n5 and zarr
    # axes = axes[::-1]
    result = "/".join(path_parts) + "/" + ".".join(axes)
    return result


def chunks_from_string(chunks: str):
    """
    Given a string of comma-separated integers, return a tuple of ints
    Parameters
    ----------
    chunks: e.g. "1,2,3"
    """
    return tuple(int(c) for c in chunks.split(","))


def chunk_id_to_slice(
        chunk_key: str, *, chunks: tuple, shape: tuple, delimiter: str = "."
):
    """
    Given a Zarr chunk key, return the slice of an array to extract that data
    Parameters
    ----------
    chunk_key: the desired chunk, e.g. "1.3.2"
    chunks: the desired chunking
    shape: the total array shape
    delimiter: chunk separator character
    """
    chunk_index = tuple(int(c) for c in chunk_key.split("."))

    if len(chunk_index) != len(chunks):
        raise ValueError(f"The length of chunk_index: {chunk_index} and chunks: {chunks} must be the same.")

    if len(shape) != len(chunks):
        raise ValueError(f"The length of shape: {shape} and chunks: {chunks} must be the same.")

    # TODO: more error handling maybe?
    slices = tuple(
        (slice(min(c * ci, s), min(c * (ci + 1), s)) for c, s, ci in zip(chunks, shape, chunk_index))
    )
    return slices
