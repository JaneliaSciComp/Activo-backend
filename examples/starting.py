import requests
from activo.data.start import start
import threading
import time

thread = threading.Thread(target=start)
thread.start()
time.sleep(2)
deploy_url = "http://127.0.0.1:5000/deploy/"
# result = requests.post(deploy_url, json={
#     "index_folder": "/Users/zouinkhim/Desktop/tmp/data/fly/dataset.zarr",
#     "data_type": "zarr",
#     "proposed_name": "zarr"
# })
# print(f"result: {result}")

result = requests.post(deploy_url, json={
    "index_folder": "/Users/zouinkhim/Desktop/tmp/data/fly/dataset.n5",
    "data_type": "n5",
    "proposed_name": "data_n5"
})
print(f"result: {result}")


result = requests.post(deploy_url, json={
    "index_folder": "/Users/zouinkhim/Desktop/tmp/data/fly/kleio/indexes",
    "kv_folder": "/Users/zouinkhim/Desktop/tmp/data/fly/kleio/kv",
    "data_type": "kleio",
    "proposed_name": "data_kleio"
})
print(f"result: {result}")
