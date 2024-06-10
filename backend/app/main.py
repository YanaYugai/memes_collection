from fastapi import FastAPI

app = FastAPI()


@app.get("/memes/")
def get_memes():
    pass


@app.get("/memes/{memes_id}")
def get_meme_by_id(memes_id: int):
    pass


@app.post("/memes/")
def create_meme():
    pass


@app.put("/memes/{memes_id}")
def change_meme(memes_id: int):
    pass


@app.delete("/memes/{memes_id}")
def delete_meme(memes_id: int):
    pass
