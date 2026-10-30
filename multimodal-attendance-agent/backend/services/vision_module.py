"""
Vision Module for Multimodal Attendance & Engagement Agent
Implements:
- Sustained Presence Tracking (State Machine filtering transient detections)
- Head Pose Estimation (Yaw, Pitch, Roll angles & classification)
- Inactivity Duration and Movement Pattern Analysis
- Eye State / Blink Estimation (EAR)
- Privacy-Preserving Feature Extraction
"""

import math
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class ParticipantPresenceTracker:
    """
    State machine that tracks participant presence over time.
    Distinguishes sustained classroom attendance from transient passers-by.
    """
    def __init__(self, sustained_threshold_sec: float = 30.0, transient_max_sec: float = 15.0):
        self.sustained_threshold_sec = sustained_threshold_sec
        self.transient_max_sec = transient_max_sec
        # Records: student_id -> { first_seen, last_seen, active_seconds, frame_count, state }
        self.records: Dict[str, Dict] = {}

    def update_presence(self, student_id: str, timestamp_sec: float = None) -> Dict:
        now = timestamp_sec if timestamp_sec is not None else time.time()
        
        if student_id not in self.records:
            self.records[student_id] = {
                "student_id": student_id,
                "first_seen": now,
                "first_seen_iso": datetime.fromtimestamp(now).strftime("%H:%M:%S"),
                "last_seen": now,
                "last_seen_iso": datetime.fromtimestamp(now).strftime("%H:%M:%S"),
                "active_seconds": 1.0,
                "consecutive_streak_sec": 1.0,
                "total_frames": 1,
                "status": "ACQUIRING",  # ACQUIRING -> PRESENT | ABSENT_TRANSIENT
                "is_sustained": False,
                "inactivity_duration_sec": 0.0,
                "last_movement_ts": now
            }
        else:
            rec = self.records[student_id]
            delta = now - rec["last_seen"]
            
            # If seen recently (within 4 seconds), accumulate active duration
            if delta <= 4.0:
                rec["active_seconds"] += delta
                rec["consecutive_streak_sec"] += delta
            else:
                # Interruption occurred; reset consecutive streak but retain cumulative
                rec["consecutive_streak_sec"] = 1.0
            
            rec["last_seen"] = now
            rec["last_seen_iso"] = datetime.fromtimestamp(now).strftime("%H:%M:%S")
            rec["total_frames"] += 1

            # State transition to PRESENT if sustained threshold passed
            if rec["active_seconds"] >= self.sustained_threshold_sec:
                rec["status"] = "PRESENT"
                rec["is_sustained"] = True
            elif rec["active_seconds"] < self.transient_max_sec:
                rec["status"] = "ACQUIRING"
                rec["is_sustained"] = False

        return self.records[student_id]

    def finalize_attendance(self, total_session_sec: float = 3000.0) -> List[Dict]:
        """
        Finalizes attendance statuses for all tracked individuals.
        Marks individuals who vanished before meeting threshold as ABSENT_TRANSIENT.
        """
        results = []
        for student_id, rec in self.records.items():
            active_sec = rec["active_seconds"]
            ratio = min(1.0, active_sec / max(1.0, total_session_sec))
            
            if active_sec >= self.sustained_threshold_sec:
                status = "PRESENT"
                note = f"Sustained presence confirmed ({int(active_sec)}s active, {ratio:.1%} session presence)"
                is_sustained = True
            else:
                status = "ABSENT_TRANSIENT"
                note = f"Filtered out: Transient detection only ({int(active_sec)}s < threshold {self.sustained_threshold_sec}s)"
                is_sustained = False

            results.append({
                "student_id": student_id,
                "status": status,
                "is_sustained": is_sustained,
                "first_detected": rec["first_seen_iso"],
                "last_detected": rec["last_seen_iso"],
                "sustained_duration_sec": round(active_sec, 1),
                "total_frames_tracked": rec["total_frames"],
                "presence_ratio": round(ratio, 3),
                "verification_note": note
            })
        return results


class VisionAnalyticsEngine:
    """
    Computer vision analytics for head pose, movement energy, and attention estimation.
    Designed with privacy preservation (retains only extracted spatial geometry).
    """

    @staticmethod
    def estimate_head_pose(landmarks_or_angles: Dict[str, float]) -> Dict:
        """
        Calculates head orientation from yaw, pitch, roll angles.
        Classification:
          - ATTENTIVE: Looking directly at instructor / presentation (-20 <= yaw <= 20, -15 <= pitch <= 15)
          - LOOKING_AWAY_LEFT / RIGHT: Distracted by peer or door
          - LOOKING_DOWN: Device glance, writing, or smartphone usage
          - HEAD_DROOPING: Drowsiness or sleep posture
        """
        yaw = landmarks_or_angles.get("yaw", 0.0)
        pitch = landmarks_or_angles.get("pitch", 0.0)
        roll = landmarks_or_angles.get("roll", 0.0)

        # Determine attention category
        if pitch < -35.0 or abs(roll) > 30.0:
            classification = "HEAD_DROOPING_DROWSY"
            attentive = False
            attention_score = 15.0
        elif pitch < -18.0:
            classification = "LOOKING_DOWN"
            attentive = False
            attention_score = 45.0  # Could be taking notes or phone usage
        elif abs(yaw) > 25.0:
            classification = "LOOKING_AWAY"
            attentive = False
            attention_score = 30.0
        else:
            classification = "ATTENTIVE_FORWARD"
            attentive = True
            attention_score = 95.0

        return {
            "yaw": round(yaw, 2),
            "pitch": round(pitch, 2),
            "roll": round(roll, 2),
            "classification": classification,
            "is_attentive": attentive,
            "attention_score": attention_score
        }

    @staticmethod
    def compute_movement_energy(current_bbox: List[float], previous_bbox: Optional[List[float]], fps: float = 30.0) -> Dict:
        """
        Calculates movement displacement dynamics to gauge restlessness vs stability.
        current_bbox: [x, y, width, height] normalized (0 to 1)
        """
        if not previous_bbox:
            return {"movement_energy": 0.35, "inactivity_flag": False, "category": "NORMAL_STABLE"}

        # Euclidean displacement of centroid
        curr_cx = current_bbox[0] + current_bbox[2] / 2.0
        curr_cy = current_bbox[1] + current_bbox[3] / 2.0
        prev_cx = previous_bbox[0] + previous_bbox[2] / 2.0
        prev_cy = previous_bbox[1] + previous_bbox[3] / 2.0

        displacement = math.sqrt((curr_cx - prev_cx) ** 2 + (curr_cy - prev_cy) ** 2)
        movement_energy = min(1.0, displacement * 25.0)

        if movement_energy < 0.04:
            category = "STATIC_FROZEN"
            inactivity = True
        elif movement_energy > 0.70:
            category = "HIGH_RESTLESSNESS"
            inactivity = False
        else:
            category = "NORMAL_ENGAGED"
            inactivity = False

        return {
            "movement_energy": round(movement_energy, 3),
            "inactivity_flag": inactivity,
            "category": category
        }

    @staticmethod
    def calculate_eye_aspect_ratio(ear_value: float) -> Dict:
        """
        Eye Aspect Ratio (EAR) evaluates eye openness.
        ear_value: ~0.28-0.35 = normal open; < 0.20 = blink or closed eyes
        """
        is_closed = ear_value < 0.20
        return {
            "ear": round(ear_value, 3),
            "eyes_closed": is_closed,
            "state": "CLOSED_DROWSY" if is_closed else "OPEN_ALERT"
        }
