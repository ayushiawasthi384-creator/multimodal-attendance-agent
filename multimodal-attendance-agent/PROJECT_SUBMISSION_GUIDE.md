# 🎓 Multimodal Attendance & Engagement Agent - Submission & Evaluation Guide
## AI-Powered Privacy-Preserving Classroom Intelligence System

---

## 📌 Project Overview & Purpose

In modern educational institutions and professional corporate training labs, traditional roll calls and simple fingerprint/biometric sensors fail to capture the real dynamics of learner participation and session effectiveness. 

The **Multimodal Attendance & Engagement Agent** resolves this problem by fusing **computer vision**, **acoustic signal processing**, and **agent-based AI reasoning** to:
1. Automatically track attendance using **sustained presence tracking** rather than fragile single-frame face detection, rejecting transient passer-by noise.
2. Quantify classroom dynamics in real-time across **head pose alignment**, **inactivity duration**, **vocal turn-taking**, and **acoustic noise floor**.
3. Generate **context-aware pedagogical teaching suggestions** using **Google Gemini 2.0 Flash** (with a 100% offline rule-based heuristic fallback for air-gapped institutions).
4. Provide instructors with hands-free audio alerts via a **Text-to-Speech (TTS) Engine** and an interactive **Code Executor** for statistical validation.

---

## 🚀 Step 1: Instant Standalone Testing (Zero Setup Required)

If you need to evaluate or demonstrate the application immediately without installing Python or configuring local databases:

1. Open File Explorer to:
   ```
   C:\Users\aruls\.gemini\antigravity\scratch\multimodal-attendance-agent\demo_preview\
   ```
2. Double-click **`index.html`** to open in **Google Chrome**, **Firefox**, or **Microsoft Edge**.
3. You can immediately test all 3 Scenarios and all system capabilities:
   - 📹 **Live Classroom Studio**: Click **"Start Live Webcam"** to test live browser biometric vector tracking and microphone FFT frequency spectrum, or leave it in CCTV simulator mode.
   - 📋 **Scenario 1 (Sustained Attendance)**: Inspect the state machine that verified 6 sustained attendees while rejecting *Ethan Davis* (18-second transient passer-by). Click **"Export Official CSV Roster"** to verify data export.
   - 📊 **Scenario 2 (Multimodal Dynamics)**: Review the 45-minute lecture timeline, the attention trough at minute 20, the interaction peak at minute 30 during Q&A, and the 26.4% front-to-back spatial seating gradient.
   - 💡 **Scenario 3 (AI Teaching Copilot)**: Review logged pedagogical interventions, click **"Speak Alert"** to test browser text-to-speech audio alerts, and adjust the engagement/cadence sliders to generate dynamic AI suggestions!
   - 💻 **Sandboxed Code Executor**: Select *Pearson Correlation Analysis*, click *Generate Code*, then click *Execute Python Sandbox* to review real-time computational verification.

---

## 🛠️ Step 2: Running Full-Stack Python Locally

### 2.1 Backend Setup
```bash
cd C:\Users\aruls\.gemini\antigravity\scratch\multimodal-attendance-agent\backend

# Install dependencies
pip install -r requirements.txt

# Start Flask Application
python app.py
```
- Server starts on: `http://localhost:5000`
- API Health Check: `http://localhost:5000/api/health`

### 2.2 Automated Launcher (Windows)
Double-click `start.bat` in the root folder to automatically verify folders, install dependencies, and start the application.

---

## 🐳 Step 3: Run with Docker Compose

If testing via Docker containerization:
```bash
docker-compose up --build
```
- Backend API & Web Dashboard: `http://localhost:5000`
- Standalone Preview Container: `http://localhost:8080`

---

## 📋 Step 4: Curriculum Epics Verification Matrix

| Epic | Subsystem | Implementation File | Verification & Testing Evidence |
|---|---|---|---|
| **EPIC 1: Requirements Specification & Environment Setup** | Modular architecture, environment variables, storage directories, Docker orchestration | `backend/config.py`, `.env.example`, `docker-compose.yml`, `start.bat` | Verified: Clean separation of `routes/`, `services/`, `storage/`, and `data/` with automated directory initialization. |
| **EPIC 2: Vision Module Development** | Sustained presence tracking state machine, head pose (yaw/pitch/roll), eye aspect ratio (EAR), inactivity | `backend/services/vision_module.py`, `tests/test_vision.py` | Verified in `test_vision.py`: Transient visitor (10s) marked `ABSENT_TRANSIENT`; sustained attendee (>30s) marked `PRESENT`. |
| **EPIC 3: Audio Module Development** | RMS energy (dBFS), Zero-Crossing Rate (ZCR), Voice Activity Detection (VAD), monologue vs discussion | `backend/services/audio_module.py`, `tests/test_audio.py` | Verified in `test_audio.py`: Speech vs silence discrimination, turn-taking ratio, and teacher monologue detection (>85%). |
| **EPIC 4: AI Implementation** | Google Gemini 2.0 Flash pedagogical reasoning, context-aware suggestions, TTS engine, offline fallback | `backend/services/genai_service.py`, `backend/services/tts_service.py` | Verified: Generates JSON structured suggestions with severity, actionable advice, and synthesized audio alert files. |
| **EPIC 5: Analytics and Recommendation Engine** | Multimodal Fusion Formula (55% Vision + 35% Audio + 10% Motion), Spatial Classroom Seating Heatmap | `backend/services/fusion_engine.py`, `tests/test_fusion.py` | Verified: Attention drop trigger (<60%), front-vs-back seating disparity detection, and spatial gradient analysis. |
| **EPIC 6: Interface, Testing, and Deployment** | REST API Gateway, Glassmorphic Dashboard, Live Webcam & Audio studio, Test suite | `backend/app.py`, `frontend/`, `tests/test_api.py`, `demo_preview/` | Verified: All 4 test suites pass (`pytest tests/`), responsive UI with Chart.js timeline and CSV export. |

---

## 🧪 Step 5: Verification of the 3 Curriculum Scenarios

### Scenario 1: Automated Attendance Tracking
- **Objective:** Mark attendance based on continuous sustained presence rather than single-frame detection, eliminating transient passer-by false positives.
- **Verification Test:**
  - `Chen Wei`: 2998 seconds sustained $\rightarrow$ **PRESENT (100% presence)**
  - `Beatriz Silva`: 2845 seconds sustained $\rightarrow$ **PRESENT (96% presence)**
  - `Ethan Davis`: 18 seconds transient walk-by $\rightarrow$ **REJECTED (`ABSENT_TRANSIENT`)**
  - `Hana Tanaka`: 0 biometric detections $\rightarrow$ **ABSENT**

### Scenario 2: Engagement and Session Dynamics Analysis
- **Objective:** Fuse head pose, inactivity, and acoustic signals over a 45-minute lecture timeline to identify attention drops and interaction peaks.
- **Verification Test:**
  - **Minute 0–10:** Theoretical intro (Composite Engagement: 79%–85%).
  - **Minute 15–20:** Monologue fatigue onset (Teacher monologue 94%, student inactivity 46%) $\rightarrow$ Attention drop trough at **54.3%** triggers intervention.
  - **Minute 25–30:** Think-pair-share and Q&A recovery $\rightarrow$ Interaction peak at **92.4%**.
  - **Spatial Heatmap:** Front Row (88.2%), Middle Row (75.4%), Back Row (61.8%) $\rightarrow$ 26.4% attention gradient flags spatial rebalancing alert.

### Scenario 3: AI-Driven Teaching Suggestions
- **Objective:** Assist educators with non-intrusive, context-aware pedagogical guidance and audio alerts.
- **Verification Test:**
  - `INT-01 (High Severity)`: Attention dip below 55% during math derivation $\rightarrow$ Prompt: *"Pause monologue for 60 seconds and launch a live Slido comprehension poll."* TTS synthesized into earpiece.
  - `INT-02 (Medium Severity)`: Speech delivery pace exceeds 185 wpm $\rightarrow$ Prompt: *"Slow speech velocity to 140 wpm and insert rhetorical pauses."*
  - `INT-03 (Low Severity)`: 26.4% front-to-back attention disparity $\rightarrow$ Prompt: *"Step away from the podium and circulate down the center aisle."*

---

## 🌐 Step 6: Pushing Code to GitHub

To push this codebase to your institutional or personal GitHub repository:
1. Double-click `push_to_github.bat` in the project root folder.
2. Enter your repository URL (e.g. `https://github.com/your-username/multimodal-attendance-agent.git`).
3. The script automatically executes `git init`, stages files, creates the initial milestone commit, and pushes to `main`.
