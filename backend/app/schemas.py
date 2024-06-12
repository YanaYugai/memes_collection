from pydantic import BaseModel, ConfigDict


class MemePostModel(BaseModel):
    text: str


class MemePostResponseModel(MemePostModel):
    id: int
    # image: str
    model_config = ConfigDict(from_attributes=True)
