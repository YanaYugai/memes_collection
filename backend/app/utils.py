from fastapi import Form, HTTPException, UploadFile
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from backend.app.schemas import MemePostModel


def checker(data: str = Form()):
    try:
        return MemePostModel.model_validate_json(data)
    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail=jsonable_encoder(e.errors()),
        )


def check_content_type(image: UploadFile):
    if image.content_type not in ["image/png", "image/jpeg", "image/tiff"]:
        raise HTTPException(400, detail="Invalid document type")
    return image
