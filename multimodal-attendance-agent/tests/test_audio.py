import sys
import math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from services.audio_module import AudioSignalProcessor

def test_audio_energy_and_vad():
    # Silent audio frame
    silence = [0.0001 * (i % 2) for i in range(1600)]
    silent_res = AudioSignalProcessor.compute_energy_metrics(silence)
    assert silent_res["is_active_speech"] is False
    assert silent_res["dbfs"] < -45.0

    # Active synthetic sine wave simulating speech signal (400 Hz)
    speech = [0.25 * math.sin(2 * math.pi * 400 * (i / 16000)) for i in range(1600)]
    speech_res = AudioSignalProcessor.compute_energy_metrics(speech)
    assert speech_res["is_active_speech"] is True
    assert speech_res["dbfs"] > -30.0
    print("✓ Audio energy and VAD test passed successfully.")

def test_interaction_dynamics():
    # Monologue timeline (mostly speech from one level)
    monologue_segments = [{"is_active_speech": True, "dbfs": -22.0} for _ in range(20)]
    mono_res = AudioSignalProcessor.analyze_interaction_dynamics(monologue_segments)
    assert mono_res["dominant_phase"] == "CONTINUOUS_TEACHER_MONOLOGUE"
    assert mono_res["teacher_monologue_pct"] > 0.70

    # Discussion timeline (varied volumes and speech bursts)
    disc_segments = [
        {"is_active_speech": True, "dbfs": -18.0 if i % 2 == 0 else -28.0}
        for i in range(20)
    ]
    disc_res = AudioSignalProcessor.analyze_interaction_dynamics(disc_segments)
    assert disc_res["dominant_phase"] == "ACTIVE_DISCUSSION_AND_QA"
    assert disc_res["student_interaction_pct"] >= 0.40
    print("✓ Audio interaction dynamics test passed successfully.")

if __name__ == "__main__":
    test_audio_energy_and_vad()
    test_interaction_dynamics()
