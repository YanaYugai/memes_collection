import http
import json
import random
import string

from backend.app.schemas import MemePostModel
from backend.crud import create_meme
from backend.models import Meme


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def create_random_meme(db) -> Meme:
    text = random_lower_string()
    meme_in = MemePostModel(text=text)
    return create_meme(session=db, meme_data=meme_in)


def test_get_memes(
    db,
    client,
):
    response = client.get(
        url="/memes/",
    )
    content = response.json()
    len_memes_before = len(content)
    assert response.status_code == 200
    create_random_meme(db)
    create_random_meme(db)
    response_after = client.get(
        url="/memes/",
    )
    content_after = response_after.json()
    len_memes_after = len(content_after)
    assert response.status_code == 200
    assert (len_memes_after - len_memes_before) == 2


def test_get_meme(
    db,
    client,
) -> None:
    meme = create_random_meme(db=db)
    response = client.get(url=f"/memes/{meme.id}/")
    response_data = response.json()
    assert response.status_code == http.HTTPStatus.OK
    assert meme.id == response_data["id"]
    assert meme.text == response_data["text"]


def test_get_meme_not_found(
    client,
) -> None:
    response = client.get(url="/memes/999/")
    response_data = response.json()
    assert response.status_code == http.HTTPStatus.NOT_FOUND
    assert response_data["detail"] == "Meme not found"


def test_post_meme(
    client,
) -> None:
    text = random_lower_string()
    data = {"data": json.dumps({"text": text})}
    response = client.post(url="/memes/", data=data)
    response_data = response.json()
    assert response.status_code == http.HTTPStatus.OK
    assert "id" in response_data
    assert text == response_data["text"]


def test_update_meme(client, db):
    meme = create_random_meme(db=db)
    new_text = random_lower_string()
    data = {"data": json.dumps({"text": new_text})}
    response = client.put(url=f"/memes/{meme.id}/", data=data)
    response_data = response.json()
    assert response.status_code == http.HTTPStatus.OK
    assert new_text == response_data["text"]


def test_update_meme_not_found(
    client,
) -> None:
    new_text = random_lower_string()
    data = {"data": json.dumps({"text": new_text})}
    response = client.put(url="/memes/999/", data=data)
    response_data = response.json()
    print(response_data)
    assert response.status_code == http.HTTPStatus.NOT_FOUND
    assert response_data["detail"] == "Meme not found"


def test_delete_meme_not_found(
    client,
) -> None:
    response = client.delete(url="/memes/999/")
    response_data = response.json()
    assert response.status_code == http.HTTPStatus.NOT_FOUND
    assert response_data["detail"] == "Meme not found"


def test_delete_meme(
    db,
    client,
) -> None:
    meme = create_random_meme(db=db)
    response = client.delete(url=f"/memes/{meme.id}/")
    assert response.status_code == http.HTTPStatus.NO_CONTENT
