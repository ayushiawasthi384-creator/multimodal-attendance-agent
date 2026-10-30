import json
from flask import Blueprint, jsonify, request, send_from_directory
from config import Config
from services.genai_service import GenAIPedagogyAgent
from services.image_gen_service import ClassroomVisualGenerator

analytics_bp = Blueprint("analytics", __name__)
ai_agent = GenAIPedagogyAgent()
visual_gen = ClassroomVisualGenerator()

def _load_sample_sessions():
    sample_path = Config.DATA_DIR / "sample_sessions.json"
    if sample_path.exists():
        with open(sample_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

@analytics_bp.route("/session-summary", methods=["GET"])
def get_session_summary():
    sessions = _load_sample_sessions()
    sc2 = sessions.get("scenario_2", {})
    summary = ai_agent.generate_session_summary(sc2)
    return jsonify({
        "success": True,
        "summary": summary
    })

@analytics_bp.route("/visual-card", methods=["GET"])
def get_visual_card():
    sessions = _load_sample_sessions()
    sc2 = sessions.get("scenario_2", {})
    spatial = sc2.get("spatial_heatmap", {})
    title = sc2.get("course_title", "Classroom Telemetry")
    res = visual_gen.generate_classroom_heatmap_svg(title, spatial)
    return jsonify({
        "success": True,
        "visual": res
    })

@analytics_bp.route("/files/<path:filename>", methods=["GET"])
def get_report_file(filename):
    return send_from_directory(Config.REPORTS_STORAGE, filename)
