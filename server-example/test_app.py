import pytest

import app

@pytest.fixture
def client():
    with app.app.test_client() as client:
        yield client

def test_image(client):
    rv = client.get("/")
    assert b'build' in rv.data
    assert b'passing' in rv.data