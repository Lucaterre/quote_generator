import pytest
from ..config_app import create_app

@pytest.fixture
def client():
    app = create_app(mode='test')
    with app.test_client() as client:
        yield client
