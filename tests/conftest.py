
import pytest

from fastapi.testclient import TestClient

from jobscout.core.config import (
    Settings,
    get_settings,
)

from jobscout.database.session import get_db
from jobscout.main import app


@pytest.fixture
def client():
    app.dependency_overrides[get_settings] = lambda: Settings(
        _env_file=None,
        database_url=(
            "postgresql+psycopg://"
            "unused:unused@localhost:5432/unused"
        ),
        admin_username="test-admin",
        admin_password="test-long-password",
    )

    # These tests do not require a real database.
    app.dependency_overrides[get_db] = lambda: None

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
