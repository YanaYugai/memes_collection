from pydantic import BaseModel


class MemePostModel(BaseModel):
    text: str


class MemePostResponseModel(MemePostModel):
    id: int
    image: str
