import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, FastAPI

from backend.app.schemas import MemePostModel, MemePostResponseModel
from backend.crud import (
    create_meme,
    delete_meme,
    get_meme_by_id_or_error,
    get_memes,
    put_meme,
)
from backend.database import AnnotatedSession

load_dotenv()

ENDPOINT = os.getenv("URL")
ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
BUCKET = os.getenv("BUCKET")


app = FastAPI()

router = APIRouter(prefix="/memes")

"""
def check_content_type(image: UploadFile):
    if image.content_type not in ["image/png", "image/jpeg", "image/tiff"]:
        raise HTTPException(400, detail="Invalid document type")
    return image


Image = Annotated[UploadFile, Depends(check_content_type)]


minio_handler = MinioHandler(ENDPOINT, ACCESS_KEY, SECRET_KEY, BUCKET)
"""


@router.get("/{meme_id}/")
def get_meme_by_id(session: AnnotatedSession, meme_id: int):
    meme = get_meme_by_id_or_error(session=session, meme_id=meme_id)
    # minio_handler.download_file(meme.image)
    return meme


@router.get("/")
def retrieve_memes(session: AnnotatedSession):
    return get_memes(session=session)


@router.post("/", response_model=MemePostResponseModel)
def post_meme(
    session: AnnotatedSession,
    # file: Image,
    text: MemePostModel = Depends(),
):
    # minio_handler.put_file(file.filename, file.file, file.size)
    # file_path = f"{minio_handler.client._base_url}/
    # {minio_handler.bucket}/{file.filename}"
    meme = create_meme(session=session, meme_data=text)
    return meme


@router.put("/{meme_id}/")
def change_meme(
    session: AnnotatedSession,
    meme_id: int,
    text: MemePostModel = Depends(),
):
    return put_meme(session=session, meme_data=text, meme_id=meme_id)


@router.delete("/{meme_id}/")
def delete_meme_api(session: AnnotatedSession, meme_id: int):
    return delete_meme(session=session, meme_id=meme_id)


app.include_router(router)
