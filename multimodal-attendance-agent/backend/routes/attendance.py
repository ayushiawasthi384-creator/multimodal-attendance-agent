import json
import csv
import io
from flask import Blueprint, jsonify, request, Response
from config import Config
from services.vision_module import ParticipantPresenceTracker

attendance_bp = Blueprint("attendance", __name__)

tracker = ParticipantPresenceTracker(
    sustained_threshold_sec=Config.SUSTAINED_PRESENCE_THRESHOLD_SEC,
    transient_max_sec=Config.TRANSIENT_FILTER_WINDOW_SEC
)

def _load_roster():
    roster_path = Config.DATA_DIR / "students_roster.json"
    if roster_path.exists():
        with open(roster_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def _load_sample_sessions():
    sample_path = Config.DATA_DIR / "sample_sessions.json"
    if sample_path.exists():
        with open(sample_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

@attendance_bp.route("/roster", methods=["GET"])
def get_roster():
    roster = _load_roster()
    return jsonify({
        "success": True,
        "total_enrolled": len(roster),
        "students": roster
    })

@attendance_bp.route("/session/<scenario_key>", methods=["GET"])
def get_scenario_attendance(scenario_key):
    sessions = _load_sample_sessions()
    session = sessions.get(scenario_key, sessions.get("scenario_1", {}))
    return jsonify({
        "success": True,
        "scenario_key": scenario_key,
        "session": session
    })

@attendance_bp.route("/track-presence", methods=["POST"])
def track_presence():
    """
    Live telemetry hook for camera feed updating participant presence.
    """
    data = request.get_json() or {}
    student_id = data.get("student_id")
    timestamp = data.get("timestamp")

    if not student_id:
        return jsonify({"error": "student_id is required"}), 400

    record = tracker.update_presence(student_id, timestamp)
    return jsonify({
        "success": True,
        "record": record
    })

@attendance_bp.route("/finalize", methods=["POST"])
def finalize():
    data = request.get_json() or {}
    duration = data.get("session_duration_sec", 3000.0)
    finalized = tracker.finalize_attendance(duration)
    return jsonify({
        "success": True,
        "finalized_attendance": finalized
    })

@attendance_bp.route("/export/csv", methods=["GET"])
def export_csv():
    scenario = request.args.get("scenario", "scenario_1")
    sessions = _load_sample_sessions()
    session_data = sessions.get(scenario, sessions.get("scenario_1", {}))
    participants = session_data.get("participants", [])

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Student ID", "Full Name", "Roll Number", "Status",
        "Sustained Duration (s)", "First Seen", "Last Seen",
        "Presence Ratio", "Verification Note"
    ])

    for p in participants:
        writer.writerow([
            p.get("student_id"),
            p.get("name"),
            p.get("roll_no"),
            p.get("status"),
            p.get("sustained_duration_sec"),
            p.get("first_detected"),
            p.get("last_detected"),
            p.get("presence_ratio"),
            p.get("verification_note")
        ])

    csv_data = output.getvalue()
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename=attendance_{scenario}_{session_data.get('session_id', 'export')}.csv"}
    )
