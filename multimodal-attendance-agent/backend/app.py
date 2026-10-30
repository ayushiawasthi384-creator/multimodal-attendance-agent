import os
from flask import Flask, render_template, jsonify, send_from_directory
from flask_cors import CORS
from pathlib import Path
from config import Config

def create_app():
    # Initialize storage directories
    Config.init_directories()

    frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
    template_folder = frontend_dir / "templates"
    static_folder = frontend_dir / "static"

    app = Flask(
        __name__,
        template_folder=str(template_folder),
        static_folder=str(static_folder),
        static_url_path="/static"
    )

    app.config.from_object(Config)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register Route Handlers (Blueprints)
    from routes.attendance import attendance_bp
    from routes.engagement import engagement_bp
    from routes.audio_analysis import audio_bp
    from routes.ai_suggestions import suggestions_bp
    from routes.code_execution import code_bp
    from routes.analytics import analytics_bp

    app.register_blueprint(attendance_bp, url_prefix="/api/attendance")
    app.register_blueprint(engagement_bp, url_prefix="/api/engagement")
    app.register_blueprint(audio_bp, url_prefix="/api/audio")
    app.register_blueprint(suggestions_bp, url_prefix="/api/suggestions")
    app.register_blueprint(code_bp, url_prefix="/api/code")
    app.register_blueprint(analytics_bp, url_prefix="/api/analytics")

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/api/health")
    def health_check():
        return jsonify({
            "status": "HEALTHY",
            "system": "Multimodal Attendance & Engagement Agent",
            "version": "2.0.0",
            "epics_supported": 6,
            "offline_mode_ready": True,
            "gemini_model": Config.GEMINI_MODEL
        })

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found", "status_code": 404}), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "Internal server error", "status_code": 500}), 500

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
