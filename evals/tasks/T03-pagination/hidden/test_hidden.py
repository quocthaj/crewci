import pytest
from fastapi.testclient import TestClient
from todo_api.app import create_app


@pytest.fixture
def client() -> TestClient:
    return TestClient(create_app())


def _make(client, count):
    for i in range(1, count + 1):
        client.post("/todos", json={"title": f"t{i}"})


def test_limit(client):
    _make(client, 5)
    response = client.get("/todos", params={"limit": 2})
    assert [t["id"] for t in response.json()] == [1, 2]


def test_offset_and_limit(client):
    _make(client, 5)
    response = client.get("/todos", params={"offset": 2, "limit": 2})
    assert [t["id"] for t in response.json()] == [3, 4]


def test_offset_beyond_end_returns_empty_list(client):
    _make(client, 3)
    response = client.get("/todos", params={"offset": 10})
    assert response.status_code == 200
    assert response.json() == []


def test_default_limit_is_50(client):
    _make(client, 60)
    assert len(client.get("/todos").json()) == 50


@pytest.mark.parametrize("limit", [0, 101, -1])
def test_invalid_limit_returns_422(client, limit):
    assert client.get("/todos", params={"limit": limit}).status_code == 422


def test_negative_offset_returns_422(client):
    assert client.get("/todos", params={"offset": -1}).status_code == 422


def test_pagination_applies_after_done_filter(client):
    for i in range(1, 7):
        client.post("/todos", json={"title": f"t{i}", "done": i % 2 == 0})
    response = client.get("/todos", params={"done": "true", "limit": 2, "offset": 1})
    assert [t["title"] for t in response.json()] == ["t4", "t6"]
