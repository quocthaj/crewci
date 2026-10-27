import pytest
from fastapi.testclient import TestClient
from todo_api.app import create_app


@pytest.fixture
def client() -> TestClient:
    return TestClient(create_app())


def test_patch_done_false_reopens_completed_todo(client):
    created = client.post("/todos", json={"title": "a", "done": True}).json()
    response = client.patch(f"/todos/{created['id']}", json={"done": False})
    assert response.status_code == 200
    assert response.json()["done"] is False
    assert client.get(f"/todos/{created['id']}").json()["done"] is False


def test_patch_done_true_still_works(client):
    created = client.post("/todos", json={"title": "a"}).json()
    response = client.patch(f"/todos/{created['id']}", json={"done": True})
    assert response.json()["done"] is True


def test_partial_update_keeps_other_fields(client):
    created = client.post("/todos", json={"title": "a", "done": True}).json()
    response = client.patch(f"/todos/{created['id']}", json={"title": "b"})
    assert response.json() == {"id": created["id"], "title": "b", "done": True}


def test_empty_patch_changes_nothing(client):
    created = client.post("/todos", json={"title": "a", "done": True}).json()
    response = client.patch(f"/todos/{created['id']}", json={})
    assert response.json() == created
