import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Verify the server is running."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "wall-robot-planner"}

def test_create_plan():
    """Verify we can submit a job."""
    payload = {
        "wall_width": 5.0,
        "wall_height": 5.0,
        "obstacles": [{"x": 2.0, "y": 2.0, "width": 1.0, "height": 1.0}]
    }
    response = client.post("/api/plan", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "PENDING"

def test_get_trajectory_404():
    """Verify error handling for non-existent jobs."""
    response = client.get("/api/trajectory/99999")
    assert response.status_code == 404

def test_response_times():
    """Validate response times for API endpoints."""
    # Health check should be fast
    start = time.time()
    response = client.get("/")
    elapsed = time.time() - start
    assert response.status_code == 200
    assert elapsed < 0.1  # Should respond in under 100ms
    
    # Job creation should be fast (returns immediately, processing is async)
    payload = {
        "wall_width": 5.0,
        "wall_height": 5.0,
        "obstacles": []
    }
    start = time.time()
    response = client.post("/api/plan", json=payload)
    elapsed = time.time() - start
    assert response.status_code == 200
    assert elapsed < 0.5  # Should respond quickly even with DB write

