from fastapi.testclient import TestClient
from fin_analytics.api.main import app

client = TestClient(app)

def test_health_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_ingest_prices():
    payload = [{
        "security_id": "BOND_001",
        "price_date": "2026-01-14",
        "clean_price": 101.25,
        "ytm": 0.052
    }]
    r = client.post("/ingest/prices", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["received"] == 1
    assert body["first"]["security_id"] == "BOND_001"
