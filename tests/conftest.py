import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.config import settings


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def api_headers():
    return {
        "X-API-Key": settings.API_KEY
    }