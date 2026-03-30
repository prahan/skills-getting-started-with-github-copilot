import copy
import pytest
from fastapi.testclient import TestClient
import src.app as app_module
from src.app import app


@pytest.fixture(autouse=True)
def reset_activities():
    """Restore the in-memory activities dict to its original state after each test."""
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(original)


@pytest.fixture
def client():
    return TestClient(app)
