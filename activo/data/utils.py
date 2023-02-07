def invert_dimensions_n5_zarr(array_metadata):
    if 'dimensions' in array_metadata:
        array_metadata['dimensions'] = array_metadata['dimensions'][::-1]
    if 'blockSize' in array_metadata:
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
    axes = axes[::-1]
    result = "/".join(path_parts) + "/" + ".".join(axes)
    return result
