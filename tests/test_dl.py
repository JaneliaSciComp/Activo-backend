import unittest
from fastapi.testclient import TestClient


class DLTestCase(unittest.TestCase):
    def test_create_model(self):
        self.assertEqual(True, False)  # add assertion here

    def test_predict(self):
        self.assertEqual(True, False)

    def test_train(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
