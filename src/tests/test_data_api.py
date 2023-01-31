import unittest
from fastapi.testclient import TestClient
from src.activo.data.start import App
import tempfile
import os
from .utils import *

app = App()
client = TestClient(app)

temp_dir = tempfile.TemporaryDirectory()
tmp = tempfile.mkdtemp()
index_path = os.path.join(tmp, "index_folder")
kv_path = os.path.join(tmp, "kv_folder")


class APIStreamDataTestCase(unittest.TestCase):
    def test_api(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_exist(self):
        response = client.get("/deploy/not_exist")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"path": "not_exist",
                                           "status": "ERROR"})

    def test_deploy_valid(self):
        create_kleio(index_path, kv_path, "test")
        self.assertTrue(os.path.exists(index_path))
        self.assertTrue(os.path.exists(kv_path))

        response = client.post("/deploy/",
                               json={"index_folder": index_path,
                                     "kv_folder": kv_path,
                                     "dataset": "test",
                                     "proposed_name": "exist_now"}
                               )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"name": "exist_now",
                                           "status": "SUCCESS"})

        response = client.get("/deploy/exist_now")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"path": "exist_now",
                                           "status": "SUCCESS"})

    def test_deploy_invalid_exist(self):
        response = client.post("/deploy/",
                               json={"index_folder": index_path,
                                     "kv_folder": kv_path,
                                     "dataset": "test",
                                     "proposed_name": "exist_now"}
                               )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"name": "exist_now",
                                           "status": "ERROR"})

    def test_deploy_invalid(self):
        response = client.post("/deploy/not_exist_before",
                               json={"index_folder": "non_valid",
                                     "kv_folder": "non_valid",
                                     "dataset": "test",
                                     "proposed_name": "exist_now"}
                               )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"name": "exist_now",
                                           "status": "ERROR"})

    def test_read(self):
        self.assertEqual(True, False)

    def test_set_annotation(self):
        self.assertEqual(True, False)

    def test_lazy_get_prediction(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
