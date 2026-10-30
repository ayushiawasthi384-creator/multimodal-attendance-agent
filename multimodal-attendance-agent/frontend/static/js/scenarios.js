/**
 * Pre-configured Scenarios Data & Simulators
 * Supports:
 * - Scenario 1: Automated Attendance Tracking (Sustained vs Transient)
 * - Scenario 2: Engagement and Session Dynamics Analysis (Multimodal Fusion)
 * - Scenario 3: AI-Driven Teaching Suggestions (Gemini 2.0 Flash & Copilot)
 */

window.CLASSROOM_SCENARIOS = {
  scenario_1: {
    id: "scenario_1",
    name: "Scenario 1: Automated Attendance Tracking",
    tagline: "Sustained Presence Tracking vs Transient Intrusion Filtering",
    threshold_sec: 30,
    session_title: "CS401: Advanced AI & Robotics",
    instructor: "Dr. Elena Rostova",
    students: [
      {
        id: "STU-001",
        name: "Aarav Sharma",
        roll: "CS2026-042",
        status: "PRESENT",
        sustained_sec: 2978,
        first_seen: "09:00:14",
        last_seen: "09:49:52",
        ratio: 0.99,
        note: "Verified: Continuous presence detected (99% frame retention)",
        avatar: "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=100"
      },
      {
        id: "STU-002",
        name: "Beatriz Silva",
        roll: "CS2026-015",
        status: "PRESENT",
        sustained_sec: 2845,
        first_seen: "09:01:05",
        last_seen: "09:48:30",
        ratio: 0.96,
        note: "Verified: Entered 1 min late, steady attention maintained",
        avatar: "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=100"
      },
      {
        id: "STU-003",
        name: "Chen Wei",
        roll: "CS2026-089",
        status: "PRESENT",
        sustained_sec: 2998,
        first_seen: "09:00:02",
        last_seen: "09:50:00",
        ratio: 1.0,
        note: "Verified: Full-session sustained presence",
        avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100"
      },
      {
        id: "STU-004",
        name: "Daria Petrova",
        roll: "CS2026-031",
        status: "PRESENT",
        sustained_sec: 2630,
        first_seen: "09:03:20",
        last_seen: "09:47:10",
        ratio: 0.88,
        note: "Verified: Brief hall break at min 25, re-acquired successfully",
        avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100"
      },
      {
        id: "STU-005",
        name: "Ethan Davis (Transient Walk-By)",
        roll: "CS2026-064",
        status: "ABSENT_TRANSIENT",
        sustained_sec: 18,
        first_seen: "09:12:04",
        last_seen: "09:12:22",
        ratio: 0.006,
        note: "REJECTED: 18s transient detection only (< 30s threshold). Pass-by filtered out.",
        avatar: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100"
      },
      {
        id: "STU-006",
        name: "Fatima Al-Mansoor",
        roll: "CS2026-077",
        status: "PRESENT",
        sustained_sec: 2990,
        first_seen: "09:00:10",
        last_seen: "09:50:00",
        ratio: 0.99,
        note: "Verified: Front row sustained participant",
        avatar: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100"
      },
      {
        id: "STU-007",
        name: "Gabriel Santos",
        roll: "CS2026-022",
        status: "PRESENT",
        sustained_sec: 2610,
        first_seen: "09:05:40",
        last_seen: "09:49:10",
        ratio: 0.87,
        note: "Verified: Sustained presence confirmed",
        avatar: "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=100"
      },
      {
        id: "STU-008",
        name: "Hana Tanaka",
        roll: "CS2026-053",
        status: "ABSENT",
        sustained_sec: 0,
        first_seen: "--",
        last_seen: "--",
        ratio: 0.0,
        note: "ABSENT: Zero biometric frames acquired",
        avatar: "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=100"
      }
    ]
  },

  scenario_2: {
    id: "scenario_2",
    name: "Scenario 2: Engagement & Dynamics Analysis",
    tagline: "Multimodal Fusion: Vision Pose + Vocal Interaction + Motion Energy",
    overall_score: 76.4,
    timeline: [
      { min: 0, phase: "Intro & Objectives", vision: 82, monologue: 65, inactivity: 10, fusion: 79.2 },
      { min: 5, phase: "Transformer Theory", vision: 88, monologue: 78, inactivity: 8, fusion: 85.6 },
      { min: 10, phase: "Mathematical Proof", vision: 79, monologue: 82, inactivity: 15, fusion: 78.4 },
      { min: 15, phase: "Monologue Fatigue", vision: 68, monologue: 89, inactivity: 28, fusion: 67.1 },
      { min: 20, phase: "Attention Trough (Alert)", vision: 52, monologue: 94, inactivity: 46, fusion: 54.3 },
      { min: 25, phase: "Peer Discussion Prompt", vision: 74, monologue: 50, inactivity: 12, fusion: 76.8 },
      { min: 30, phase: "Active Q&A & Code Demo", vision: 91, monologue: 40, inactivity: 9, fusion: 92.4 },
      { min: 35, phase: "Implementation", vision: 84, monologue: 68, inactivity: 14, fusion: 82.0 },
      { min: 40, phase: "Hands-on Exercise", vision: 77, monologue: 58, inactivity: 16, fusion: 79.5 },
      { min: 45, phase: "Summary & Wrapup", vision: 81, monologue: 62, inactivity: 12, fusion: 80.7 }
    ],
    spatial_heatmap: {
      front_row: { name: "Row 1 (Front)", avg_engagement: 88.2, distraction: 5 },
      middle_row: { name: "Row 2 (Middle)", avg_engagement: 75.4, distraction: 16 },
      back_row: { name: "Row 3 (Back)", avg_engagement: 61.8, distraction: 32 }
    }
  },

  scenario_3: {
    id: "scenario_3",
    name: "Scenario 3: AI Teaching Suggestions",
    tagline: "Context-Aware Pedagogical Interventions with Gemini & TTS",
    interventions: [
      {
        id: "INT-01",
        time: "09:20:15",
        severity: "HIGH",
        category: "Pacing & Energy",
        title: "Inject Interactive Checkpoint / Quick Poll",
        body: "Attention dropped by 28% in the middle and back rows during theoretical derivation. Pause your monologue for 60 seconds and launch a live comprehension poll.",
        tts_alert: "Attention dip detected across back rows. Pause for a 60-second interactive poll.",
        impact: "Engagement surged from 54% to 77% within 4 minutes."
      },
      {
        id: "INT-02",
        time: "09:33:40",
        severity: "MEDIUM",
        category: "Vocal Dynamics",
        title: "Vocal Modulation & Cadence Adjustment",
        body: "Your delivery pace reached 185 words/minute with low vocal inflection. Moderate speech velocity to 140 wpm and use deliberate rhetorical pauses.",
        tts_alert: "Delivery pace is rapid at 185 words per minute. Ease speed and insert a pause.",
        impact: "Note-taking activity increased by 34%."
      },
      {
        id: "INT-03",
        time: "09:42:10",
        severity: "LOW",
        category: "Classroom Dynamics",
        title: "Physical Proximity Rebalancing",
        body: "Noticeable attention gradient between front and back rows. Step away from the lectern and walk down the center aisle towards Row 3 to re-engage peripheral students.",
        tts_alert: "Noticeable attention gradient. Move towards the center aisle near Row 3.",
        impact: "Back row head pose alignment shifted to 82% attentive."
      }
    ]
  }
};
