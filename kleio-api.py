from kleio.stores import VersionedFSStore, ZarrIndexStore
import zarr

from flask import Flask
from flask import request
from zarr.n5 import invert_chunk_coords
app = Flask(__name__)

from flask_cors import CORS
from zarr.n5 import invert_chunk_coords

CORS(app)

path = '/Users/zouinkhim/Desktop/tmp/data_demo_versioned'
path_index = '/Users/zouinkhim/Desktop/tmp/index_demo_versioned'

index_store = ZarrIndexStore(path_index)
store = VersionedFSStore(index_store, path)


# z = zarr.open(store)

def is_unformatted_chunk(path: str):
    if "." in path:
        return False
    if "/" not in path:
        return False
    elms = path.split("/")
    if len(elms) <= 1:
        return False
    if elms[-1].isdigit():
        return True
    return False


def format_key(path):
    if not is_unformatted_chunk(path):
        return path
    elms = path.split("/")
    result = ""
    for elm in elms:
        if str(elm).isdigit():
            result += elm + "."
        else:
            result += elm + "/"
    return result[:-1]


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path: str):
    print(f"getting: {path}")
    path = format_key(invert_chunk_coords(format_key(path)))
    print(f"after format: {path}")
    if "0.3.2" in path :
        print("hi1")

    if "2.3.0" in path:
        print("hi2")
    try:
        result = store[path]
        print(f"works: {path}")
        return result
    except:
        print(f"error: {path}")
        return "error", 404


if __name__ == '__main__':
    app.run()
