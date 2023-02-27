import json
from enum import Enum

import zarr
from fastapi import HTTPException, APIRouter
from kleio.stores import N5FSIndexStore, VersionedFSStore
from starlette.responses import Response
from zarr import N5FSStore

from data.utils import format_chunk_n5_to_zarr_key
from .base import ActiveBaseModel

router = APIRouter(
    prefix="/data",
    tags=["data"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


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

    def __str__(self) -> str:
        return f" index_folder = {self.index_folder} - kv_folder = {self.kv_folder}"


class PostAnnotationRequest(ActiveBaseModel):
    path: str
    data: bytes


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


# TODO change to SQL base
_deployed_data = dict()


# Deploy local data to be accessible using HTTP
@router.post("/deploy/")
async def deploy_data(request: PostDeployDataRequest):
    print(f"DeployDataRequest: {request}")
    if request.proposed_name in _deployed_data:
        raise HTTPException(status_code=404,
                            detail="Already exist")
    try:
        reader = create_reader(request)
        _deployed_data[request.proposed_name] = DeployedData(request, reader)
        return {"name": request.proposed_name}
    except Exception as ex:
        raise HTTPException(status_code=404,
                            detail=f"can't create reader: {ex}")


@router.get("/all/")
async def get_all_deployed_data():
    result = {}
    for name in _deployed_data:
        result[name] = str(_deployed_data[name])
    return result


# Check if data exists, if yes return the deployment name
@router.get("/deploy/")
async def get_deployed_data(request: GetDeployedDataRequest):
    try:
        print(f"GetDeployedDataRequest: {request}")
        for value in _deployed_data.values():
            if value == request:
                return {"name": value.name}
    except Exception as ex:
        raise HTTPException(status_code=404,
                            detail=f"Error: {ex}")
    raise HTTPException(status_code=404,
                        detail="Don't exist")


@router.get("/{name}/{path:path}")
async def get_data(name: str, path: str):
    print(f" data {name} - path {path}")

    if name not in _deployed_data:
        raise HTTPException(status_code=404,
                            detail="Don't exist")
    try:
        reader = _deployed_data[name].reader
        data_type = _deployed_data[name].data_type
        is_chunk = False
        last_element = path.split("/")[-1]
        if last_element.isdigit() or last_element.split(".")[-1].isdigit():
            is_chunk = True
        if is_chunk:
            if data_type is DataType.kleio:
                path = format_chunk_n5_to_zarr_key(path)
            result = reader[path]
            return Response(result, media_type='binary/octet-stream')
        else:
            result = reader[path]
            return json.loads(result.decode())
    except Exception as e:
        raise HTTPException(status_code=404,
                            detail=f"error {e}")


# TODO
@router.post("/annotation/")
async def post_annotation_data(request: PostAnnotationRequest):
    print(f"path {request.path}")
    return {"status": "success"}
