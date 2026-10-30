import json
from flask import Blueprint, jsonify, request
from config import Config
from services.fusion_engine import MultimodalFusionEngine
from services.vision_module import VisionAnalyticsEngine

engagement_bp = Blueprint("engagement", __name__)
fusion_engine = MultimodalFusionEngine()

def _load_sample_sessions():
    sample_path = Config.DATA_DIR / "sample_sessions.json"
    if sample_path.exists():
        with open(sample_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

@engagement_bp.route("/timeline/<scenario_key>", methods=["GET"])
def get_timeline(scenario_key):
    sessions = _load_sample_sessions()
    scenario = sessions.get(scenario_key, sessions.get("scenario_2", {}))
    return jsonify({
        "success": True,
        "scenario": scenario
    })

@engagement_bp.route("/fuse-telemetry", methods=["POST"])
def fuse_telemetry():
    """
    Receives current vision & audio telemetry slice and fuses them into an engagement metric.
    """
    data = request.get_json() or {}
    vision_metrics = data.get("vision", {})
    audio_metrics = data.get("audio", {})
    motion_metrics = data.get("motion", {})

    fusion_result = fusion_engine.fuse_interval(vision_metrics, audio_metrics, motion_metrics)
    return jsonify({
        "success": True,
        "fusion": fusion_result
    })

@engagement_bp.route("/spatial-heatmap", methods=["GET"])
def get_spatial_heatmap():
    sessions = _load_sample_sessions()
    sc2 = sessions.get("scenario_2", {})
    spatial = sc2.get("spatial_heatmap", {
        "front_row": {"attendance": 3, "avg_engagement": 88.2, "distraction_rate": 0.05},
        "middle_row": {"attendance": 3, "avg_engagement": 75.4, "distraction_rate": 0.16},
        "back_row": {"attendance": 2, "avg_engagement": 61.8, "distraction_rate": 0.32}
    })
    analysis = fusion_engine.calculate_spatial_gradient(spatial)

    return jsonify({
        "success": True,
        "spatial_heatmap": spatial,
        "analysis": analysis
    })

@engagement_bp.route("/estimate-head-pose", methods=["POST"])
def estimate_head_pose():
    data = request.get_json() or {}
    angles = data.get("angles", {"yaw": 0.0, "pitch": 0.0, "roll": 0.0})
    result = VisionAnalyticsEngine.estimate_head_pose(angles)
    return jsonify({
        "success": True,
        "head_pose": result
    })
