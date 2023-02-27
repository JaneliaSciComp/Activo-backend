from fastapi import APIRouter

from app.routers.data import PostDeployDataRequest

# prediction pool: agent waiting for make prediction and send back
router = APIRouter(
    prefix="/lazy",
    tags=["lazy"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


class PostDeployLazyRequest(PostDeployDataRequest):
    raw_path: str
    model_path: str
    branch_name: str


# TODO
@router.post("/deploy/")
async def deploy_lazy_prediction(request: PostDeployLazyRequest):
    return {}


# TODO
@router.get("/{name}/{path:path}")
async def get_lazy_prediction_data(name: str, path: str):
    print(f" data {name} - path {path}")
    return {"status": "success"}
