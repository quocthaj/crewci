import pytest
from fastapi.testclient import TestClient
from todo_api.app import create_app


@pytest.fixture
def client() -> TestClient:
    return TestClient(create_app())


def _seed(client):
    client.post("/todos", json={"title": "a", "done": True})
    client.post("/todos", json={"title": "b", "done": False})
    client.post("/todos", json={"title": "c", "done": True})


def test_done_true_returns_only_completed(client):
    _seed(client)
    response = client.get("/todos", params={"done": "true"})
    assert response.status_code == 200
    assert [t["title"] for t in response.json()] == ["a", "c"]


def test_done_false_returns_only_open(client):
    _seed(client)
    response = client.get("/todos", params={"done": "false"})
    assert [t["title"] for t in response.json()] == ["b"]


def test_without_filter_returns_everything(client):
    _seed(client)
    response = client.get("/todos")
    assert [t["title"] for t in response.json()] == ["a", "b", "c"]
