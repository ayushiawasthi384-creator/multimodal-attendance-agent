import json
from flask import Blueprint, jsonify, request
from config import Config
from services.genai_service import GenAIPedagogyAgent
from services.tts_service import TextToSpeechService

suggestions_bp = Blueprint("suggestions", __name__)
ai_agent = GenAIPedagogyAgent()
tts_service = TextToSpeechService()

def _load_sample_sessions():
    sample_path = Config.DATA_DIR / "sample_sessions.json"
    if sample_path.exists():
        with open(sample_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

@suggestions_bp.route("/active-interventions", methods=["GET"])
def get_interventions():
    sessions = _load_sample_sessions()
    sc3 = sessions.get("scenario_3", {})
    interventions = sc3.get("active_interventions", [])
    return jsonify({
        "success": True,
        "interventions": interventions
    })

@suggestions_bp.route("/generate", methods=["POST"])
def generate_suggestion():
    """
    Generates a context-aware teaching suggestion based on real-time classroom telemetry.
    Uses Google Gemini 2.0 Flash when API key is configured, or offline pedagogy rule engine.
    """
    data = request.get_json() or {}
    metrics = data.get("metrics", {
        "composite_engagement_score": 54.0,
        "vision_attention_score": 52.0,
        "audio_interaction_score": 58.0,
        "cadence_wpm": 178,
        "is_attention_drop": True
    })
    phase = data.get("session_phase", "Theoretical Monologue")

    suggestion = ai_agent.generate_teaching_suggestion(metrics, phase)

    # Synthesize audio if requested
    tts_result = None
    if data.get("synthesize_tts", True) and "tts_alert" in suggestion:
        tts_result = tts_service.generate_speech_file(suggestion["tts_alert"])

    return jsonify({
        "success": True,
        "suggestion": suggestion,
        "audio_alert": tts_result
    })

@suggestions_bp.route("/synthesize-audio", methods=["POST"])
def synthesize_audio():
    data = request.get_json() or {}
    text = data.get("text", "Classroom attention alert.")
    alert_id = data.get("alert_id")

    res = tts_service.generate_speech_file(text, alert_id)
    return jsonify(res)
