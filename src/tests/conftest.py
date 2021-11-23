import pytest
from starlette.testclient import TestClient

from app.main import app

#https://www.lambdatest.com/blog/end-to-end-tutorial-for-pytest-fixtures-with-examples/
@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client  # testing happens here