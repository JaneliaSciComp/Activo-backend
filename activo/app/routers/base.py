from pydantic import BaseModel


# TODO remove dataset and have API work regardless to dataset ex. localhost/PROPOSED_NAME/dataset
class ActiveBaseModel(BaseModel):
    class Config:
        orm_mode = True
