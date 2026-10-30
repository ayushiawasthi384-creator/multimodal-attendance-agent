import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from services.vision_module import ParticipantPresenceTracker, VisionAnalyticsEngine

def test_sustained_presence_tracking():
    tracker = ParticipantPresenceTracker(sustained_threshold_sec=30.0, transient_max_sec=15.0)

    # 1. Simulate Transient student (walks by for only 10 seconds)
    base_ts = 1000.0
    for s in range(0, 10, 2):
        tracker.update_presence("STU-TRANSIENT", base_ts + s)

    # 2. Simulate Sustained student (stays in classroom for 40 seconds)
    for s in range(0, 42, 2):
        tracker.update_presence("STU-SUSTAINED", base_ts + s)

    finalized = tracker.finalize_attendance(total_session_sec=100.0)
    results_map = {r["student_id"]: r for r in finalized}

    # Verify transient visitor was rejected from attendance
    assert results_map["STU-TRANSIENT"]["status"] == "ABSENT_TRANSIENT"
    assert results_map["STU-TRANSIENT"]["is_sustained"] is False

    # Verify sustained attendee was marked PRESENT
    assert results_map["STU-SUSTAINED"]["status"] == "PRESENT"
    assert results_map["STU-SUSTAINED"]["is_sustained"] is True
    print("✓ Sustained presence test passed successfully.")

def test_head_pose_estimation():
    # Forward looking attentive
    attentive = VisionAnalyticsEngine.estimate_head_pose({"yaw": 4.5, "pitch": -2.0, "roll": 1.0})
    assert attentive["is_attentive"] is True
    assert attentive["classification"] == "ATTENTIVE_FORWARD"

    # Looking away distracted
    distracted = VisionAnalyticsEngine.estimate_head_pose({"yaw": 32.0, "pitch": 0.0, "roll": 0.0})
    assert distracted["is_attentive"] is False
    assert distracted["classification"] == "LOOKING_AWAY"

    # Drowsy / drooping head
    drowsy = VisionAnalyticsEngine.estimate_head_pose({"yaw": 0.0, "pitch": -38.0, "roll": 10.0})
    assert drowsy["is_attentive"] is False
    assert drowsy["classification"] == "HEAD_DROOPING_DROWSY"
    print("✓ Head pose estimation test passed successfully.")

def test_movement_energy():
    bbox1 = [0.2, 0.2, 0.1, 0.1]
    bbox2 = [0.201, 0.201, 0.1, 0.1]
    static_res = VisionAnalyticsEngine.compute_movement_energy(bbox2, bbox1)
    assert static_res["inactivity_flag"] is True

    bbox3 = [0.35, 0.35, 0.1, 0.1]
    moving_res = VisionAnalyticsEngine.compute_movement_energy(bbox3, bbox1)
    assert moving_res["inactivity_flag"] is False
    print("✓ Movement dynamics test passed successfully.")

if __name__ == "__main__":
    test_sustained_presence_tracking()
    test_head_pose_estimation()
    test_movement_energy()
