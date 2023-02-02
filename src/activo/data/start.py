import json
import os

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from zarr.storage import FSStore

from .utils import *

description = """
Activo for Active learning  
"""


# ## Items
#
# You can **read items**.
#
# ## Users
#
# You will be able to:
#
# * **Create users** (_not implemented_).
# * **Read users** (_not implemented_).

# TODO remove dataset and have API work regardless to dataset ex. localhost/PROPOSED_NAME/dataset
class ActiveBaseModel(BaseModel):
    class Config:
        orm_mode = True


class PostDeployDataRequest(ActiveBaseModel):
    index_folder: str
    kv_folder: str
    proposed_name: str


class GetDeployedDataRequest(ActiveBaseModel):
    index_folder: str
    kv_folder: str


class DeployedData:
    def __init__(self, request: PostDeployDataRequest, reader) -> None:
        self.index_folder = request.index_folder
        self.kv_folder = request.kv_folder
        self.name = request.proposed_name
        self.reader = reader

    def __eq__(self, o: object) -> bool:
        if self.index_folder != o.index_folder:
            return False
        if self.kv_folder != o.kv_folder:
            return False
        return True


class App(FastAPI):

    def __init__(self) -> None:
        super().__init__(title="Activo",
                         description=description,
                         version="0.0.1",
                         terms_of_service="http://example.com/terms/",
                         # contact={
                         #     "name": "Marwan Zouinkhi",
                         #     "url": "https://github.com/mzouink",
                         #     "email": "zouinkhi.marwan@gmail.com",
                         # },
                         license_info={
                             "name": "Apache 2.0",
                             "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
                         },
                         docs_url="/")
        self.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self._deployed_data = dict()

        # Deploy local data to be accessible using HTTP
        @self.post("/deploy/")
        async def deploy_data(request: PostDeployDataRequest):
            print(f"DeployDataRequest: {request}")
            if request.proposed_name in self._deployed_data:
                raise HTTPException(status_code=404,
                                    detail="Already exist")
            try:
                reader = create_kleio_dataset_reader(request.index_folder,
                                                     request.kv_folder)
                self._deployed_data[request.proposed_name] = DeployedData(request, reader)
                return {"name": request.proposed_name}
            except Exception as ex:
                raise HTTPException(status_code=404,
                                    detail=f"can't create reader: {ex}")

        # Check if data exists, if yes return the deployment name
        @self.get("/deploy/")
        async def get_deployed_data(request: GetDeployedDataRequest):
            try:
                print(f"GetDeployedDataRequest: {request}")
                for value in self._deployed_data.values():
                    if value == request:
                        return {"name": value.name}
            except Exception as ex:
                raise HTTPException(status_code=404,
                                    detail=f"Error: {ex}")
            raise HTTPException(status_code=404,
                                detail="Don't exist")

        # No dataset specified so Group metadata .zgroup
        @self.get("/data/{name}/attributes.json")
        def get_attributes(name: str) -> dict:
            if name not in self._deployed_data:
                raise HTTPException(status_code=404,
                                    detail="Don't exist")
            index_folder = self._deployed_data[name].kv_folder
            store = FSStore(index_folder)
            return json.loads(store["attributes.json"].decode())
            # return Response(bytes(store["attributes.json"].decode(), 'utf-8'), media_type='binary/octet-stream')

        @self.get("/data/{name}/{path:path}/attributes.json")
        def get_dataset_attributes(name: str, path: str) -> dict:
            if name not in self._deployed_data:
                raise HTTPException(status_code=404,
                                    detail="Don't exist")
            index_folder = self._deployed_data[name].kv_folder
            store = FSStore(index_folder)
            path_new = os.path.join(path, "attributes.json")
            return format_array_meta_fix_n5(json.loads(store[path_new].decode()))

        @self.get("/data/{name}/{path:path}/{chunk_key}")
        def get_chunk(
                name: str, path: str, chunk_key: str) -> bytes:

            print(f"Getting chunk: {path}")
            path_new = format_chunk_n5_to_zarr_key(os.path.join(path, chunk_key))
            print(f"formatted_path: {path_new}")
            print(f'Host: {name}, Path: {path}')
            store = self._get_store(data=name)
            # try:
            data = store[path_new]
            # application/octet-stream

            return Response(data, media_type='binary/octet-stream')
            # except Exception as ex:
            #     raise HTTPException(status_code=404,
            #                         detail=f"Error: {ex}")

        # @self.get("/data/{name}/{path:path}")
        # async def get_data(name: str, path: str):
        #     print(f" data {name} - path {path}")
        #
        #     # if len(elms) <= 1:
        #     #     raise HTTPException(status_code=404,
        #     #                         detail="Need to specify element")
        #     name = elms[0]
        #     if name not in self._deployed_data:
        #         raise HTTPException(status_code=404,
        #                             detail="Don't exist")
        #
        #     reader = self._deployed_data[name].reader
        #     rest_path = "/".join(elms[1:])
        #     print(f"Got reader {reader}")
        #     print(f"Rest path {rest_path}")
        #     result = reader[rest_path]
        #     if isinstance(result, str):
        #         return json_loads(result)
        #     else:
        #         return result

        # @self.get("/data/lazy/{path:path}")
        # async def get_lazy_prediction_data(path: str):
        #     print(f"path {path}")
        #     return {"status": "success"}
        #
        # @self.post("/data/annotation/{path:path}")
        # async def post_annotation_data(path: str):
        #     print(f"path {path}")
        #     return {"status": "success"}

    def _get_store(self, data):
        if data not in self._deployed_data:
            raise HTTPException(status_code=404,
                                detail="Don't exist")
        return self._deployed_data[data].reader


def start():
    app = App()
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")
