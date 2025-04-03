import pytest
from app import app, dvc_add_and_push
import tempfile
import os

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_upload_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Upload CSV File" in response.data

def test_dvc_operations():
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
        tmp.write(b"col1,col2\n1,2\n3,4")
        tmp_path = tmp.name
    
    try:
        assert dvc_add_and_push(tmp_path) is True
    finally:
        os.unlink(tmp_path)
        if os.path.exists(f"{tmp_path}.dvc"):
            os.unlink(f"{tmp_path}.dvc")