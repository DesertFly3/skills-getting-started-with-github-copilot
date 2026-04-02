from fastapi.testclient import TestClient
import pytest

from src.app import activities, app, build_initial_activities


@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange
    activities.clear()
    activities.update(build_initial_activities())

    yield

    # Arrange
    activities.clear()
    activities.update(build_initial_activities())


@pytest.fixture
def client():
    # Arrange
    return TestClient(app)
