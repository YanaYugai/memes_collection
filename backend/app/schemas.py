from fastapi import Form, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict, ValidationError


class MemePostModel(BaseModel):
    text: str


class MemePostResponseModel(MemePostModel):
    id: int
    image: str
    model_config = ConfigDict(from_attributes=True)


def checker(data: str = Form()):
    try:
        return MemePostModel.model_validate_json(data)
    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail=jsonable_encoder(e.errors()),
        )
