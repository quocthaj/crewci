from fastapi.testclient import TestClient

from dashboard.app import app


def test_health_ok_and_db_created(tmp_path, monkeypatch):
    db_file = tmp_path / "test.db"
    monkeypatch.setenv("CREWCI_DB_PATH", str(db_file))
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert db_file.exists()
