from fastapi import APIRouter

# Agent that go randomly to data and make prediction and create tasks for annotators
router = APIRouter(
    prefix="/crawler",
    tags=["crawler"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)