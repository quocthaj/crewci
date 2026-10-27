def test_create_todo(client):
    response = client.post("/todos", json={"title": "write docs"})
    assert response.status_code == 201
    assert response.json() == {"id": 1, "title": "write docs", "done": False}


def test_create_todo_rejects_empty_title(client):
    response = client.post("/todos", json={"title": ""})
    assert response.status_code == 422


def test_get_todo(client):
    created = client.post("/todos", json={"title": "a"}).json()
    response = client.get(f"/todos/{created['id']}")
    assert response.status_code == 200
    assert response.json() == created


def test_get_missing_todo_returns_404(client):
    assert client.get("/todos/999").status_code == 404


def test_list_todos(client):
    client.post("/todos", json={"title": "a"})
    client.post("/todos", json={"title": "b"})
    response = client.get("/todos")
    assert [t["title"] for t in response.json()] == ["a", "b"]


def test_update_title(client):
    created = client.post("/todos", json={"title": "old"}).json()
    response = client.patch(f"/todos/{created['id']}", json={"title": "new"})
    assert response.status_code == 200
    assert response.json() == {"id": created["id"], "title": "new", "done": False}


def test_mark_done(client):
    created = client.post("/todos", json={"title": "a"}).json()
    response = client.patch(f"/todos/{created['id']}", json={"done": True})
    assert response.json()["done"] is True


def test_update_missing_todo_returns_404(client):
    assert client.patch("/todos/999", json={"title": "x"}).status_code == 404
