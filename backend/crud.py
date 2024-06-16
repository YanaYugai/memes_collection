from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.schemas import MemePostModel
from models import Meme


def get_meme_by_id_or_error(session: Session, meme_id: int):
    meme = session.get(Meme, meme_id)
    if not meme:
        raise HTTPException(status_code=404, detail="Meme not found")
    return meme


def get_memes(session: Session):
    memes = session.scalars(select(Meme)).all()
    return memes


def create_meme(session: Session, meme_data: MemePostModel, image: str):
    meme = Meme(**meme_data.model_dump(), image=image)
    session.add(meme)
    session.commit()
    session.refresh(meme)
    return meme


def put_meme(
    session: Session,
    meme_data: MemePostModel,
    meme: Meme,
    image: str,
):
    meme_query = session.query(Meme).where(Meme.id == meme.id)
    meme_data_dict = meme_data.model_dump()
    meme_data_dict["image"] = image
    meme_query.update(meme_data_dict)  # type: ignore
    session.commit()
    session.refresh(meme)
    return meme


def delete_meme(session: Session, meme: Meme):
    session.delete(meme)
    session.commit()
