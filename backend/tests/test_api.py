from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_content():
    response = client.post("/content/", json={"topic": "AI", "audience": "developers", "platform": "blog"})
    assert response.status_code == 200
    assert "content" in response.json()
