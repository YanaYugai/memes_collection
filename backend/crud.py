from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.schemas import MemePostModel
from backend.models import Meme


def get_meme_by_id_or_error(session: Session, meme_id: int):
    meme = session.get(Meme, meme_id)
    if not meme:
        raise HTTPException(status_code=404, detail="Meme not found")
    return meme


def get_memes(session: Session):
    memes = session.scalars(select(Meme)).all()
    return memes


def create_meme(session: Session, meme_data: MemePostModel):
    meme = Meme(**meme_data.model_dump())
    session.add(meme)
    session.commit()
    session.refresh(meme)
    return meme


def put_meme(
    session: Session,
    meme_data: MemePostModel,
    meme_id: int,
    # image: str,
):
    meme = session.query(Meme).where(Meme.id == meme_id)
    meme_instance = meme.one_or_none()  # type: ignore
    if not meme_instance:
        raise HTTPException(status_code=404, detail="Meme not found")
    meme_data_dict = meme_data.model_dump()
    # meme_data_dict["image"] = image
    meme.update(meme_data_dict)  # type: ignore
    session.commit()
    session.refresh(meme_instance)
    return meme_instance


def delete_meme(session: Session, meme_id: int):
    meme = get_meme_by_id_or_error(session, meme_id)
    session.delete(meme)
    session.commit()
