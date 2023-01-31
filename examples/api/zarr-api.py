import zarr

from flask import Flask
from flask import request

app = Flask(__name__)

from flask_cors import CORS

CORS(app)

path_zarr = '/Users/zouinkhim/Desktop/tmp/zarr'

z = zarr.open(path_zarr, mode="a")
store = z.store


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
    app.run()
