import http
import json
import random
import string


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def create_random_meme(client) -> dict[str, str]:
    text = random_lower_string()
    data = {"data": json.dumps({"text": text})}
    with open("carbon felt.jpg", "rb") as image:
        response = client.post(
            url="/memes/",
            data=data,
            files={"image": image},
        )
        response_data = response.json()
    return response_data


def test_paginator(
    client,
):
    params = {"size": 2}
    response = client.get(
        url="/memes/",
        params=params,
    )
    content = response.json()
    assert response.status_code == 200
    assert "items" in content
    assert "total" in content
    assert "page" in content
    assert "pages" in content


def test_get_meme(
    client,
) -> None:
    meme = create_random_meme(client=client)
    response = client.get(url=f"/memes/{meme['id']}/")
    response_data = response.json()
    assert response.status_code == http.HTTPStatus.OK
    assert meme["id"] == response_data["id"]
    assert meme["text"] == response_data["text"]


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
    with open("carbon felt.jpg", "rb") as image:
        response = client.post(
            url="/memes/",
            data=data,
            files={"image": image},
        )
        response_data = response.json()
        assert response.status_code == http.HTTPStatus.OK
        assert "id" in response_data
        assert text == response_data["text"]
        assert "image" in response_data


def test_post_meme_without_text(
    client,
) -> None:
    with open("carbon felt.jpg", "rb") as image:
        response = client.post(
            url="/memes/",
            files={"image": image},
        )
        assert response.status_code == http.HTTPStatus.UNPROCESSABLE_ENTITY


def test_download_meme(
    client,
) -> None:
    text = random_lower_string()
    data = {"data": json.dumps({"text": text})}
    with open("carbon felt.jpg", "rb") as image:
        response = client.post(
            url="/memes/",
            data=data,
            files={"image": image},
        )
        response_data = response.json()
    response_image = client.get(f'{response_data["image"]}')
    assert response_image.status_code == http.HTTPStatus.OK


def test_update_meme(client):
    meme = create_random_meme(client=client)
    new_text = random_lower_string()
    data = {"data": json.dumps({"text": new_text})}
    with open("fibers.png", "rb") as image:
        response = client.put(
            url=f"/memes/{meme['id']}/",
            data=data,
            files={'image': image},
        )
        response_data = response.json()
        assert response.status_code == http.HTTPStatus.OK
        assert new_text == response_data["text"]
        assert meme["image"] != response_data["image"]


def test_update_meme_not_found(
    client,
) -> None:
    new_text = random_lower_string()
    data = {"data": json.dumps({"text": new_text})}
    with open("fibers.png", "rb") as image:
        response = client.put(
            url="/memes/999/",
            data=data,
            files={"image": image},
        )
    response_data = response.json()
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
    client,
) -> None:
    meme = create_random_meme(client=client)
    response = client.delete(url=f"/memes/{meme['id']}/")
    assert response.status_code == http.HTTPStatus.NO_CONTENT


def test_get_memes(
    client,
):
    params = {"size": 2}
    response = client.get(
        url="/memes/",
        params=params,
    )
    content = response.json()
    len_memes_before = content["total"]
    for _ in range(5):
        create_random_meme(client)
    response_after = client.get(
        url="/memes/",
        params=params,
    )
    len_memes_after = response_after.json()["total"]
    assert response_after.status_code == 200
    assert (len_memes_after - len_memes_before) == 5
