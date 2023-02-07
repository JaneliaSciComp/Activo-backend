import tensorflow as tf
from tensorflow import keras


def example_model():
    return tf.keras.applications.MobileNetV2(input_shape=[128, 128, 3], include_top=False)


# Loads the weights
# model.load_weights(checkpoint_path)

def load_model(path):
    pass


class Model(object):
    def __init__(self, path: str):
        self._path = path

    def _load(self):
        self._model = load_model(self._path)
