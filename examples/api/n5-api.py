import zarr

from flask import Flask
from flask import request

app = Flask(__name__)

from flask_cors import CORS

CORS(app)

path_zarr = '/Users/zouinkhim/Desktop/tmp/n5'

store = zarr.n5.N5FSStore(path_zarr)
# z = zarr.open(path_zarr, mode="a")
# store = z.store


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path: str):
    print(f"getting: {path}")
    try:
        # result = z[path]
        result = store[path]
        print(f"works: {path}")
        return result
    except:
        print(f"error: {path}")
        return "error", 404


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
