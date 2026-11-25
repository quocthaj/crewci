import pytest
from fastapi.testclient import TestClient
from todo_api.app import create_app


@pytest.fixture
def client() -> TestClient:
    return TestClient(create_app())


def test_delete_returns_204_with_empty_body(client):
    created = client.post("/todos", json={"title": "a"}).json()
    response = client.delete(f"/todos/{created['id']}")
    assert response.status_code == 204
    assert response.content == b""


def test_deleted_todo_is_gone(client):
    created = client.post("/todos", json={"title": "a"}).json()
    client.delete(f"/todos/{created['id']}")
    assert client.get(f"/todos/{created['id']}").status_code == 404
    assert client.get("/todos").json() == []


def test_delete_missing_returns_404_with_detail(client):
    response = client.delete("/todos/999")
    assert response.status_code == 404
    assert "detail" in response.json()


def test_ids_are_not_reused(client):
    client.post("/todos", json={"title": "a"})
    second = client.post("/todos", json={"title": "b"}).json()
    deleted = client.delete(f"/todos/{second['id']}")
    assert deleted.status_code == 204
    third = client.post("/todos", json={"title": "c"}).json()
    assert third["id"] == second["id"] + 1


def test_delete_leaves_other_todos_untouched(client):
    first = client.post("/todos", json={"title": "a"}).json()
    second = client.post("/todos", json={"title": "b"}).json()
    client.delete(f"/todos/{second['id']}")
    assert client.get("/todos").json() == [first]
