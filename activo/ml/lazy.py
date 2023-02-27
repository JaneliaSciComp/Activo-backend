# from kleio.stores import VersionedFSStore
# from .model import Model
# from zarr.storage import Store
#
# class LazyLoader:
#     def __init__(self,
#                  current_version: int,
#                  store_input: Store,
#                  dataset_input : str,
#                  store_output: VersionedFSStore,
#                  dataset_output : str,
#                  model: Model) -> None:
#         self._current_version = current_version
#         self._store_output = store_output
#         self._model = model
#         self._dataset_output = dataset_output
#         self.__pending_blocks = list()
#         self.__saving_queue = list()
#
#     async def get_block(self, grid_position: [int]):
#         if grid_position in self.__pending_blocks:
#             block
#         if grid_position in self.__saving_queue:
#             return block
#         if self._store._index[grid_position] == self._current_version:
#             get block from store
#         return block = self._predict(grid_position)
#         save_block(block,grid_position)
#
#     def _predict(self, grid_position):
#         input_block = load_input_block(grid_position)
#         output = self._model.predict(input_block)
#         return output
#
#
# # block thread
# from threading import Thread
# from threading import Lock
# import sys
#
# class Counter:
#
#     def __init__(self):
#         self.count = 0
#         self.lock = Lock()
#
#     def increment(self):
#         for _ in range(100000):
#             self.lock.acquire()
#             self.count += 1
#             self.lock.release()
#
# # wait until
# https://stackoverflow.com/questions/2785821/is-there-an-easy-way-in-python-to-wait-until-certain-condition-is-true
#
