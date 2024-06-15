from typing import Any, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi_pagination import add_pagination
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from backend import models
from backend.app.main import router
from backend.database import get_db

TEST_SQL_DB = "sqlite:///./test_db.db"

engine = create_engine(TEST_SQL_DB, connect_args={"check_same_thread": False})

SessionTest = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def start_application():
    app = FastAPI()
    app.include_router(router)
    add_pagination(app)
    return app


@pytest.fixture(scope="session", autouse=True)
def app() -> Generator[FastAPI, Any, None]:
    models.Base.metadata.create_all(bind=engine)
    _app = start_application()
    yield _app
    models.Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, Any, None]:
    models.Base.metadata.create_all(bind=engine)
    with SessionTest() as session:
        yield session
    models.Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def client(
    app: FastAPI,
) -> Generator[TestClient, None, None]:
    def _get_test_db():
        with SessionTest() as session:
            yield session

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client
