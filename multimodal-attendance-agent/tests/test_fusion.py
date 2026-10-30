import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from services.fusion_engine import MultimodalFusionEngine

def test_fusion_formula():
    engine = MultimodalFusionEngine(weight_vision=0.55, weight_audio=0.35, weight_motion=0.10)

    # High attention + engaging discussion + normal motion
    vision = {"head_pose_attentive_pct": 90.0}
    audio = {"speech_activity_ratio": 0.70, "teacher_monologue_pct": 0.50, "student_interaction_pct": 0.40}
    motion = {"inactivity_pct": 12.0}

    result = engine.fuse_interval(vision, audio, motion)
    assert result["composite_engagement_score"] >= 85.0
    assert result["is_attention_drop"] is False
    assert result["alert_level"] == "OPTIMAL" or result["alert_level"] == "GOOD"
    print("✓ Fusion formula high engagement test passed.")

def test_attention_drop_detection():
    engine = MultimodalFusionEngine(weight_vision=0.55, weight_audio=0.35, weight_motion=0.10)

    # Disengaged scenario: looking down/away, monologue fatigue, high inactivity
    vision = {"head_pose_attentive_pct": 45.0}
    audio = {"speech_activity_ratio": 0.95, "teacher_monologue_pct": 0.95, "student_interaction_pct": 0.05}
    motion = {"inactivity_pct": 48.0}

    result = engine.fuse_interval(vision, audio, motion)
    assert result["composite_engagement_score"] < 60.0
    assert result["is_attention_drop"] is True
    assert result["pedagogical_status"] == "ATTENTION_DROP_ALERT"
    print("✓ Attention drop trigger test passed.")

def test_spatial_gradient():
    grid = {
        "front_row": {"avg_engagement": 88.0},
        "middle_row": {"avg_engagement": 74.0},
        "back_row": {"avg_engagement": 58.0}
    }
    analysis = MultimodalFusionEngine.calculate_spatial_gradient(grid)
    assert analysis["front_vs_back_disparity"] == 30.0
    assert analysis["needs_physical_rebalancing"] is True
    print("✓ Spatial gradient test passed.")

if __name__ == "__main__":
    test_fusion_formula()
    test_attention_drop_detection()
    test_spatial_gradient()
