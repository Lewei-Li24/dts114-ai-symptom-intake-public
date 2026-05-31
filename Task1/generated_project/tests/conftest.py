import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app, init_db


@pytest.fixture()
def app(tmp_path):
    test_app = create_app(
        {
            "TESTING": True,
            "DATABASE": str(tmp_path / "test_symptom_triage.db"),
            "AI_API_KEY": None,
        }
    )
    init_db(test_app)
    return test_app


@pytest.fixture()
def client(app):
    return app.test_client()
