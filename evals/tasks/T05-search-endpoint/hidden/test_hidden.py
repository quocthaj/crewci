import pytest
from fastapi.testclient import TestClient
from todo_api.app import create_app


@pytest.fixture
def client() -> TestClient:
    return TestClient(create_app())


def _seed(client):
    for title in ["Buy milk", "Walk the dog", "milk the cow", "Read book"]:
        client.post("/todos", json={"title": title})


def test_search_is_case_insensitive_substring_match(client):
    _seed(client)
    response = client.get("/todos/search", params={"q": "MILK"})
    assert response.status_code == 200
    assert [t["title"] for t in response.json()] == ["Buy milk", "milk the cow"]


def test_search_without_match_returns_empty_list(client):
    _seed(client)
    response = client.get("/todos/search", params={"q": "zzz"})
    assert response.status_code == 200
    assert response.json() == []


def test_search_requires_q(client):
    assert client.get("/todos/search").status_code == 422
    assert client.get("/todos/search", params={"q": ""}).status_code == 422


def test_get_by_id_still_works(client):
    _seed(client)
    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Buy milk"
