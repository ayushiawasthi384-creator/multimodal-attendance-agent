"""
Multimodal Fusion Engine (EPIC 5)
Fuses computer vision behavioral indicators with acoustic interaction signals
into a synchronized, temporal classroom engagement matrix.
"""

from typing import Dict, List, Optional

class MultimodalFusionEngine:
    def __init__(self, weight_vision: float = 0.55, weight_audio: float = 0.35, weight_motion: float = 0.10):
        self.w_vision = weight_vision
        self.w_audio = weight_audio
        self.w_motion = weight_motion

    def fuse_interval(
        self,
        vision_metrics: Dict,
        audio_metrics: Dict,
        inactivity_metrics: Optional[Dict] = None
    ) -> Dict:
        """
        Fuses a temporal slice of vision + audio signals into composite engagement indicators.
        """
        # 1. Vision component (0 - 100)
        # Based on % of students with attentive head pose + eye alert state
        attentive_pct = vision_metrics.get("head_pose_attentive_pct", 75.0)
        vision_score = max(0.0, min(100.0, attentive_pct))

        # 2. Audio component (0 - 100)
        # Optimal learning is an active, balanced vocal interaction (~60-75% speech with discussion)
        # Heavy monologues (>90%) or extended dead silence (<15%) reduce score
        speech_ratio = audio_metrics.get("speech_activity_ratio", 0.60)
        monologue_pct = audio_metrics.get("teacher_monologue_pct", 0.50)
        student_int_pct = audio_metrics.get("student_interaction_pct", 0.30)
        
        if speech_ratio < 0.15:
            # Extended silence lull
            audio_score = 45.0
        elif monologue_pct > 0.85:
            # Droning monologue without questions
            audio_score = 58.0
        elif student_int_pct >= 0.35:
            # Active two-way discussion & Q&A
            audio_score = 94.0
        else:
            # Steady, engaging presentation
            audio_score = 80.0

        # 3. Motion Dynamics component (0 - 100)
        # Inactivity < 20% is good; motionless freezing > 40% or wild restless agitation > 70% drops score
        inactivity_pct = 15.0
        if inactivity_metrics:
            inactivity_pct = inactivity_metrics.get("inactivity_pct", 15.0)
        elif "inactivity_pct" in vision_metrics:
            inactivity_pct = vision_metrics["inactivity_pct"]

        if inactivity_pct > 40.0:
            # Heavy drowsiness or disengagement
            motion_score = max(20.0, 100.0 - (inactivity_pct * 1.5))
        elif inactivity_pct < 5.0:
            # High fidgeting
            motion_score = 70.0
        else:
            motion_score = 88.0

        # Weighted Multimodal Fusion
        composite_score = (
            (vision_score * self.w_vision) +
            (audio_score * self.w_audio) +
            (motion_score * self.w_motion)
        )
        composite_score = round(max(0.0, min(100.0, composite_score)), 1)

        # Pedagogical Alert Flagging
        is_attention_drop = composite_score < 60.0 or (attentive_pct < 60.0 and monologue_pct > 0.80)
        is_interaction_peak = composite_score >= 88.0 and student_int_pct >= 0.30

        if is_attention_drop:
            status = "ATTENTION_DROP_ALERT"
            level = "WARNING"
        elif is_interaction_peak:
            status = "INTERACTION_PEAK"
            level = "OPTIMAL"
        elif composite_score >= 75.0:
            status = "HIGH_ENGAGEMENT"
            level = "GOOD"
        else:
            status = "MODERATE_ENGAGEMENT"
            level = "NORMAL"

        return {
            "composite_engagement_score": composite_score,
            "vision_attention_score": round(vision_score, 1),
            "audio_interaction_score": round(audio_score, 1),
            "motion_stability_score": round(motion_score, 1),
            "is_attention_drop": is_attention_drop,
            "is_interaction_peak": is_interaction_peak,
            "pedagogical_status": status,
            "alert_level": level
        }

    @staticmethod
    def calculate_spatial_gradient(grid_data: Dict) -> Dict:
        """
        Calculates spatial attention drop-off between front row, middle row, and back row.
        """
        front_eng = grid_data.get("front_row", {}).get("avg_engagement", 85.0)
        back_eng = grid_data.get("back_row", {}).get("avg_engagement", 60.0)
        disparity = round(front_eng - back_eng, 1)

        needs_rebalancing = disparity > 20.0

        return {
            "front_vs_back_disparity": disparity,
            "needs_physical_rebalancing": needs_rebalancing,
            "recommendation": (
                "High front-to-back attention gradient detected. Instructor advised to circulate toward back rows."
                if needs_rebalancing else "Spatial attention distribution is relatively balanced."
            )
        }
