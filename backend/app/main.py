from typing import Annotated

from fastapi import Depends, FastAPI, File
from schemas import MemePostModel, MemePostResponseModel

app = FastAPI()


@app.get("/memes/")
def get_memes():
    pass


@app.get("/memes/{memes_id}")
def get_meme_by_id(meme_id: int):
    pass


@app.post("/memes/", response_model=MemePostResponseModel)
def create_meme(
    file: Annotated[bytes, File()],
    meme: MemePostModel = Depends(),
):
    pass


@app.put("/memes/{memes_id}")
def change_meme(meme_id: int):
    pass


@app.delete("/memes/{memes_id}")
def delete_meme(meme_id: int):
    pass
