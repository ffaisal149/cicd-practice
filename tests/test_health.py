from fastapi.testclient import TestClient

import app.main as main

client = TestClient(main.app)


def test_health_is_ok_when_database_answers():
    assert client.get("/health").status_code == 200


def test_health_is_503_when_database_is_down(monkeypatch):
    class BrokenEngine:
        def connect(self):
            raise ConnectionError("database down")

    monkeypatch.setattr(main, "get_engine", lambda: BrokenEngine())
    response = client.get("/health")
    assert response.status_code == 503
