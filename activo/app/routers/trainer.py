from fastapi import APIRouter

# continuous learner, keep training model
router = APIRouter(
    prefix="/train",
    tags=["train"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)