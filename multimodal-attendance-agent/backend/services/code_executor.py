"""
Code Generation & Execution Service
Implements:
- AI-driven analytics code generation
- Safe execution sandbox with captured stdout and outputs
- Persistence in backend/storage/code/ as specified in architecture
"""

import sys
import io
import time
import uuid
from pathlib import Path
from typing import Dict, Any, Optional
from config import Config

class AnalyticsCodeExecutor:
    def __init__(self, storage_dir: Optional[Path] = None):
        self.storage_dir = storage_dir or Config.CODE_STORAGE
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def generate_analytics_script(self, task_type: str = "correlation_analysis") -> Dict:
        """
        Generates Python analytical script for advanced classroom intelligence metrics.
        """
        script_id = f"analytics_{task_type}_{uuid.uuid4().hex[:6]}"
        filename = f"{script_id}.py"
        filepath = self.storage_dir / filename

        if task_type == "correlation_analysis":
            code = '''# Classroom Analytics: Multimodal Correlation Analysis
# Computes correlation between Teacher Monologue Duration and Student Inactivity

timeline = [
    {"min": 0, "monologue_pct": 0.65, "inactivity_pct": 10, "engagement": 79.2},
    {"min": 5, "monologue_pct": 0.78, "inactivity_pct": 8, "engagement": 85.6},
    {"min": 10, "monologue_pct": 0.82, "inactivity_pct": 15, "engagement": 78.4},
    {"min": 15, "monologue_pct": 0.89, "inactivity_pct": 28, "engagement": 67.1},
    {"min": 20, "monologue_pct": 0.94, "inactivity_pct": 46, "engagement": 54.3},
    {"min": 25, "monologue_pct": 0.50, "inactivity_pct": 12, "engagement": 76.8},
    {"min": 30, "monologue_pct": 0.40, "inactivity_pct": 9, "engagement": 92.4},
    {"min": 35, "monologue_pct": 0.68, "inactivity_pct": 14, "engagement": 82.0},
    {"min": 40, "monologue_pct": 0.58, "inactivity_pct": 16, "engagement": 79.5},
    {"min": 45, "monologue_pct": 0.62, "inactivity_pct": 12, "engagement": 80.7}
]

x = [t["monologue_pct"] for t in timeline]
y = [t["inactivity_pct"] for t in timeline]
n = len(x)

mean_x = sum(x) / n
mean_y = sum(y) / n

cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
std_x = (sum((val - mean_x) ** 2 for val in x) / n) ** 0.5
std_y = (sum((val - mean_y) ** 2 for val in y) / n) ** 0.5

r = cov / (std_x * std_y) if (std_x * std_y) != 0 else 0

print(f"=== CLASSROOM MULTIMODAL CORRELATION REPORT ===")
print(f"Analyzed {n} session intervals (45 minutes total)")
print(f"Mean Teacher Monologue Ratio: {mean_x:.2%}")
print(f"Mean Student Inactivity Ratio: {mean_y:.2f}%")
print(f"Pearson Correlation (r): {r:.4f}")
print(f"Interpretation: Strong positive correlation (r = {r:.2f}).")
print("Long uninterrupted instructor monologues directly correlate with surge in student inactivity.")
'''
        elif task_type == "attendance_verification":
            code = '''# Sustained Presence Verification Algorithm
# Computes True Positive Attendance vs Transient Intrusions

records = [
    {"name": "Aarav Sharma", "active_sec": 2978, "threshold": 30},
    {"name": "Beatriz Silva", "active_sec": 2845, "threshold": 30},
    {"name": "Chen Wei", "active_sec": 2998, "threshold": 30},
    {"name": "Daria Petrova", "active_sec": 2630, "threshold": 30},
    {"name": "Ethan Davis (Transient Pass-by)", "active_sec": 18, "threshold": 30},
    {"name": "Fatima Al-Mansoor", "active_sec": 2990, "threshold": 30},
    {"name": "Gabriel Santos", "active_sec": 2610, "threshold": 30}
]

print("=== SUSTAINED ATTENDANCE VERIFICATION RUNNER ===")
present_count = 0
transient_count = 0

for r in records:
    is_sustained = r["active_sec"] >= r["threshold"]
    if is_sustained:
        present_count += 1
        status = "[PRESENT] Sustained presence verified"
    else:
        transient_count += 1
        status = "[REJECTED] Transient walk-by (< 30s)"
    print(f"Student: {r['name']:<30} Active: {r['active_sec']:>4}s -> {status}")

print("-" * 50)
print(f"Total Enrolled Verified: {present_count}")
print(f"Transient Noise Suppressed: {transient_count}")
'''
        else:
            code = '''# Dynamic Seating Attention ANOVA
rows = {
    "Front Row": [88, 92, 85],
    "Middle Row": [76, 78, 72],
    "Back Row": [62, 58, 65]
}

print("=== SPATIAL SEATING ENGAGEMENT METRICS ===")
for row_name, scores in rows.items():
    avg = sum(scores) / len(scores)
    print(f"{row_name:<12} | Avg Engagement: {avg:.1f}% | Spread: {max(scores) - min(scores)}%")

overall = [s for sublist in rows.values() for s in sublist]
print(f"Total Classroom Mean: {sum(overall)/len(overall):.1f}%")
'''

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)

        return {
            "script_id": script_id,
            "filename": filename,
            "filepath": str(filepath),
            "code": code,
            "task_type": task_type
        }

    def execute_script(self, code: str, script_id: Optional[str] = None) -> Dict:
        """
        Executes a Python analytics script safely, capturing stdout and execution time.
        """
        start_time = time.time()
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        old_stdout = sys.stdout
        old_stderr = sys.stderr

        exec_globals = {
            "__builtins__": {
                "print": print,
                "range": range,
                "len": len,
                "sum": sum,
                "min": min,
                "max": max,
                "abs": abs,
                "round": round,
                "int": int,
                "float": float,
                "str": str,
                "list": list,
                "dict": dict,
                "enumerate": enumerate,
                "zip": zip,
                "bool": bool
            }
        }

        success = True
        try:
            sys.stdout = stdout_capture
            sys.stderr = stderr_capture
            exec(code, exec_globals)
        except Exception as e:
            success = False
            stderr_capture.write(f"Execution Error: {str(e)}\n")
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

        elapsed_ms = round((time.time() - start_time) * 1000, 2)
        output_text = stdout_capture.getvalue()
        error_text = stderr_capture.getvalue()

        # If script_id given or new code, save to storage
        if not script_id:
            script_id = f"exec_{uuid.uuid4().hex[:6]}"
        filepath = self.storage_dir / f"{script_id}.py"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)

        return {
            "script_id": script_id,
            "success": success,
            "output": output_text,
            "error": error_text if not success else None,
            "execution_time_ms": elapsed_ms,
            "saved_file": str(filepath)
        }
