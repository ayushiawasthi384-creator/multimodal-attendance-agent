import os
from flask import Blueprint, jsonify, request, send_from_directory, current_app
from config import Config
from services.audio_module import AudioSignalProcessor

audio_bp = Blueprint("audio", __name__)

@audio_bp.route("/analyze-samples", methods=["POST"])
def analyze_samples():
    """
    Receives raw audio PCM float samples from Web Audio API or audio feed.
    """
    data = request.get_json() or {}
    samples = data.get("samples", [])
    sample_rate = data.get("sample_rate", 16000)

    result = AudioSignalProcessor.compute_energy_metrics(samples, sample_rate)
    return jsonify({
        "success": True,
        "metrics": result
    })

@audio_bp.route("/analyze-session-timeline", methods=["POST"])
def analyze_session_timeline():
    data = request.get_json() or {}
    segments = data.get("segments", [])
    window = data.get("window_minutes", 5.0)

    interaction = AudioSignalProcessor.analyze_interaction_dynamics(segments, window)
    return jsonify({
        "success": True,
        "interaction": interaction
    })

@audio_bp.route("/files/<path:filename>", methods=["GET"])
def get_audio_file(filename):
    """
    Serves generated audio files from backend/storage/audio/
    """
    return send_from_directory(Config.AUDIO_STORAGE, filename)
