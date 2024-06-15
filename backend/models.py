from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Meme(Base):
    __tablename__ = "memes"

    id: Mapped[int] = mapped_column(primary_key=True)
    image: Mapped[str]
    text: Mapped[str]
