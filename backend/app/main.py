import os
from typing import Annotated, cast

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, FastAPI, UploadFile
from fastapi_pagination import Page, add_pagination, paginate
from starlette.responses import StreamingResponse

from app.schemas import MemePostModel, MemePostResponseModel
from app.utils import check_content_type, checker
from crud import (
    create_meme,
    delete_meme,
    get_meme_by_id_or_error,
    get_memes,
    put_meme,
)
from database import AnnotatedSession
from minio_api.minio_handler import MinioHandler

load_dotenv()

ENDPOINT = cast(str, os.getenv("ENDPOINT"))
API_ENDPOINT = cast(str, os.getenv("API_ENDPOINT"))
ACCESS_KEY = cast(str, os.getenv("ACCESS_KEY"))
SECRET_KEY = cast(str, os.getenv("SECRET_KEY"))
BUCKET = cast(str, os.getenv("BUCKET"))


app = FastAPI()

router = APIRouter(prefix="/memes")


Image = Annotated[UploadFile, Depends(check_content_type)]


minio_handler = MinioHandler(
    ENDPOINT,
    API_ENDPOINT,
    ACCESS_KEY,
    SECRET_KEY,
    BUCKET,
)


@router.get("/{meme_id}/")
def get_meme_by_id(session: AnnotatedSession, meme_id: int):
    meme = get_meme_by_id_or_error(session=session, meme_id=meme_id)
    return meme


@router.get("/")
def retrieve_memes(session: AnnotatedSession) -> Page[MemePostResponseModel]:
    memes = get_memes(session=session)
    return paginate(memes)


@router.post("/", response_model=MemePostResponseModel)
def post_meme(
    session: AnnotatedSession,
    file: Image,
    text: MemePostModel = Depends(checker),
):
    url = minio_handler.put_file(file.filename, file.file, file.size)
    meme = create_meme(session=session, meme_data=text, image=url)
    return meme


@router.put("/{meme_id}/")
def change_meme(
    session: AnnotatedSession,
    meme_id: int,
    file: Image,
    text: MemePostModel = Depends(checker),
):
    meme = get_meme_by_id_or_error(session=session, meme_id=meme_id)
    minio_handler.remove_file(meme.image)
    url = minio_handler.put_file(file.filename, file.file, file.size)
    return put_meme(session=session, meme_data=text, meme=meme, image=url)


@router.delete("/{meme_id}/", status_code=204)
def delete_meme_api(session: AnnotatedSession, meme_id: int):
    meme = get_meme_by_id_or_error(session=session, meme_id=meme_id)
    minio_handler.remove_file(meme.image)
    delete_meme(session=session, meme=meme)


@router.get('/download/{temp_link}/')
async def download(temp_link: str):
    decoded_jwt = minio_handler.decode_token(temp_link)
    filename = decoded_jwt['filename']
    return StreamingResponse(
        minio_handler.download_file(filename),
        media_type='image/png',
    )


app.include_router(router)
add_pagination(app)
