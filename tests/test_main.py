import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_chat_api():
    response = client.post("/chat", json={"user_question": "What is the sum of 1 and 2?"})
    assert response.status_code == 200
    assert "result" in response.json()