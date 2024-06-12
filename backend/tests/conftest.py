from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from backend import models
from backend.app.main import app
from backend.database import engine

SessionTest = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator:
    with SessionTest() as session:
        create_tables()
        yield session


def create_tables():
    models.Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client
