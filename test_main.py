
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_list_current():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"folder_content": ["__init__.py", "main.py", "__pycache__", "README", "TestFolder", "test_main.py"]}

def test_list_folder():
    response = client.post("/ls/",json={"folder_name": "TestFolder", "delay_call": 0})
    assert response.status_code == 200
    assert response.json() == {"folder_content": ["Hello", "World"]}

def test_list_folder_nonexistent():
    response = client.post("/ls/",json={"folder_name": "HelloWorld", "delay_call": 0})
    assert response.status_code == 404
    assert response.json() == {"detail": "ls: cannot access 'HelloWorld': No such file or directory"}

def test_list_folder_no_permission():
    response = client.post("/ls/",json={"folder_name": "/root", "delay_call": 0})
    assert response.status_code == 404
    assert response.json() == {"detail": "ls: cannot open directory '/root': Permission denied"}
