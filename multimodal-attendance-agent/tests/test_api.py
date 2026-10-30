import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app import create_app

def test_api_routes():
    app = create_app()
    client = app.test_client()

    # Health check
    res = client.get("/api/health")
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data["status"] == "HEALTHY"
    print("✓ API Health Check passed.")

    # Roster endpoint
    res = client.get("/api/attendance/roster")
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data["total_enrolled"] >= 5
    print("✓ API Roster endpoint passed.")

    # Spatial heatmap endpoint
    res = client.get("/api/engagement/spatial-heatmap")
    assert res.status_code == 200
    data = json.loads(res.data)
    assert "front_row" in data["spatial_heatmap"]
    print("✓ API Spatial Heatmap endpoint passed.")

    # AI Teaching suggestion endpoint (offline fallback test)
    res = client.post("/api/suggestions/generate", json={
        "metrics": {"composite_engagement_score": 52.0, "vision_attention_score": 50.0, "is_attention_drop": True},
        "session_phase": "Theoretical Lecture",
        "synthesize_tts": True
    })
    assert res.status_code == 200
    data = json.loads(res.data)
    assert "suggestion" in data
    assert "suggestion_title" in data["suggestion"]
    print("✓ API AI Suggestion generation passed.")

    # Code Executor endpoint
    res = client.post("/api/code/generate", json={"task_type": "correlation_analysis"})
    assert res.status_code == 200
    data = json.loads(res.data)
    assert "script" in data
    code = data["script"]["code"]

    res_exec = client.post("/api/code/execute", json={"code": code})
    assert res_exec.status_code == 200
    exec_data = json.loads(res_exec.data)
    assert exec_data["result"]["success"] is True
    assert "Pearson Correlation" in exec_data["result"]["output"]
    print("✓ API Code Generation & Execution passed.")

if __name__ == "__main__":
    test_api_routes()
