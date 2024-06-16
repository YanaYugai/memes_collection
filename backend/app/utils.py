import json

from fastapi import Form, HTTPException, UploadFile
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from app.schemas import MemePostModel


def checker(text: str = Form()):
    try:
        # return MemePostModel.model_validate_json(json.dumps({"text": text}))
        return MemePostModel.model_validate_json(json.dumps({"text": text}))
    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail=jsonable_encoder(e.errors()),
        )


def check_content_type(image: UploadFile):
    if image.content_type not in [
        "image/png",
        "image/jpeg",
        "image/tiff",
        "image/gif",
    ]:
        raise HTTPException(400, detail="Invalid document type")
    return image
