from typing import Union

import numpy as np
from zarr.hierarchy import Group, Array

import zarr.n5
# TODO fix compressor, now running with default
def convert(source: Union[Group, Array],
            output: Union[Group, Array],
            compressor=None,
            chunks=None):
    print(f"Converting : {source.path}")
    if isinstance(source, Group):
        if source.path != "":
            output.create_group(source.path)
        for source_key in sorted(source.keys()):
            convert(source[source_key], output, compressor, chunks)
    elif isinstance(source, Array):
        if compressor is None:
            compressor = source.compressor
        if chunks is None:
            chunks = source.chunks
            # compressor=compressor,
        output.create_dataset(source.path, shape=source.shape, chunks=chunks,
                              dtype=np.dtype(source.dtype).str)
        output[source.path][:] = source[:]
