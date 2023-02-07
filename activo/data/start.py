import json
from enum import Enum

import uvicorn
import zarr
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from kleio.stores import VersionedFSStore, N5FSIndexStore
from pydantic import BaseModel
from zarr.n5 import N5FSStore
from starlette.responses import Response
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


class DataType(str, Enum):
    n5 = "n5"
    zarr = "zarr"
    kleio = "kleio"


# TODO extends from GET
class PostDeployDataRequest(ActiveBaseModel):
    index_folder: str
    kv_folder: str = None
    proposed_name: str
    data_type: DataType


class GetDeployedDataRequest(ActiveBaseModel):
    index_folder: str
    kv_folder: str = None


class DeployedData:
    def __init__(self, request: PostDeployDataRequest, reader) -> None:
        self.index_folder = request.index_folder
        self.kv_folder = request.kv_folder
        self.data_type = request.data_type
        self.name = request.proposed_name
        self.reader = reader

    def __eq__(self, o: object) -> bool:
        if self.index_folder != o.index_folder:
            return False
        if self.kv_folder != o.kv_folder:
            return False
        return True


def create_reader(request: PostDeployDataRequest):
    data_type = request.data_type
    if data_type == DataType.n5:
        return N5FSStore(request.index_folder)
    elif data_type == DataType.zarr:
        return zarr.open(request.index_folder).store
    elif data_type == DataType.kleio:
        if request.kv_folder is None:
            raise Exception("Kleio store needs KV path!")
        index_store = N5FSIndexStore(request.index_folder)
        store = VersionedFSStore(index_store, request.kv_folder)
        return store
    else:
        raise Exception(f"DataType {request.data_type} is not implemented!")


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
                reader = create_reader(request)
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

        @self.get("/data/{name}/{path:path}")
        async def get_kleio_data(name: str, path: str):
            print(f" data {name} - path {path}")

            if name not in self._deployed_data:
                raise HTTPException(status_code=404,
                                    detail="Don't exist")
            try:
                reader = self._deployed_data[name].reader
                data_type = self._deployed_data[name].data_type

                print(f"Got reader {reader}")

                is_chunk = False
                last_element = path.split("/")[-1]

                if last_element.isdigit() or last_element.split(".")[-1].isdigit():
                    print("is chunk")
                    is_chunk = True

                if is_chunk:
                    if data_type is DataType.kleio:
                        path = format_chunk_n5_to_zarr_key(path)
                    result = reader[path]
                    return Response(result, media_type='binary/octet-stream')
                else:
                    result = reader[path]
                    print(f"Got result {result}")
                    return json.loads(result.decode())
            except Exception as e:
                raise HTTPException(status_code=404,
                                    detail=f"error {e}")

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
    return uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")
