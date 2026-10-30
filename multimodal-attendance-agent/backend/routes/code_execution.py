from flask import Blueprint, jsonify, request
from config import Config
from services.code_executor import AnalyticsCodeExecutor

code_bp = Blueprint("code", __name__)
executor = AnalyticsCodeExecutor()

@code_bp.route("/generate", methods=["POST"])
def generate_code():
    data = request.get_json() or {}
    task_type = data.get("task_type", "correlation_analysis")
    script_data = executor.generate_analytics_script(task_type)
    return jsonify({
        "success": True,
        "script": script_data
    })

@code_bp.route("/execute", methods=["POST"])
def execute_code():
    data = request.get_json() or {}
    code = data.get("code", "")
    script_id = data.get("script_id")

    if not code.strip():
        return jsonify({"error": "No code provided to execute"}), 400

    result = executor.execute_script(code, script_id)
    return jsonify({
        "success": True,
        "result": result
    })

@code_bp.route("/saved-scripts", methods=["GET"])
def list_saved_scripts():
    scripts = []
    if Config.CODE_STORAGE.exists():
        for f in Config.CODE_STORAGE.glob("*.py"):
            scripts.append({
                "filename": f.name,
                "size_bytes": f.stat().st_size,
                "modified": f.stat().st_mtime
            })
    return jsonify({
        "success": True,
        "scripts": scripts
    })
