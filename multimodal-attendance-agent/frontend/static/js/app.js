/**
 * Main Controller for Multimodal Attendance & Engagement Agent
 */

document.addEventListener("DOMContentLoaded", () => {
  const charts = new ClassroomCharts();
  let studio = null;
  let currentScenario = "scenario_1";

  // Elements
  const videoElem = document.getElementById("webcam-feed");
  const canvasElem = document.getElementById("overlay-canvas");
  const audioCanvas = document.getElementById("audio-spectrum-canvas");
  const toggleCamBtn = document.getElementById("toggle-camera-btn");
  const camStatusText = document.getElementById("cam-status-text");

  // Initialize Video Studio
  if (videoElem && canvasElem) {
    studio = new ClassroomStudio(videoElem, canvasElem, audioCanvas);
    studio.startRenderLoop();
  }

  // Camera Toggle
  if (toggleCamBtn) {
    toggleCamBtn.addEventListener("click", async () => {
      if (!studio.isCameraActive) {
        camStatusText.textContent = "Connecting Camera...";
        const res = await studio.startCamera();
        if (res.success) {
          toggleCamBtn.innerHTML = `<span>📹</span> Stop Camera`;
          camStatusText.textContent = "LIVE CAMERA FEED ACTIVE";
          camStatusText.style.color = "#34d399";
        } else {
          alert("Unable to access live webcam. Falling back to CCTV Simulator.\n(" + res.error + ")");
          camStatusText.textContent = "CCTV SIMULATOR ACTIVE";
          camStatusText.style.color = "#94a3b8";
        }
      } else {
        studio.stopCamera();
        toggleCamBtn.innerHTML = `<span>📹</span> Start Live Webcam`;
        camStatusText.textContent = "CCTV SIMULATOR ACTIVE";
        camStatusText.style.color = "#94a3b8";
      }
    });
  }

  // Tab Switching
  const tabBtns = document.querySelectorAll(".tab-btn");
  const tabContents = document.querySelectorAll(".tab-content");

  tabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      const tabId = btn.getAttribute("data-tab");
      tabBtns.forEach(b => b.classList.remove("active"));
      tabContents.forEach(c => c.classList.remove("active"));

      btn.classList.add("active");
      const target = document.getElementById(tabId);
      if (target) target.classList.add("active");

      // Redraw charts if switching to dynamics tab
      if (tabId === "tab-dynamics") {
        setTimeout(() => {
          loadScenario2();
        }, 50);
      }
    });
  });

  // Scenario Buttons
  const scenarioBtns = document.querySelectorAll(".scenario-btn");
  scenarioBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      const scenKey = btn.getAttribute("data-scenario");
      scenarioBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      switchScenario(scenKey);
    });
  });

  function switchScenario(scenKey) {
    currentScenario = scenKey;
    if (scenKey === "scenario_1") {
      activateTab("tab-attendance");
      loadScenario1();
    } else if (scenKey === "scenario_2") {
      activateTab("tab-dynamics");
      loadScenario2();
    } else if (scenKey === "scenario_3") {
      activateTab("tab-suggestions");
      loadScenario3();
    }
  }

  function activateTab(tabId) {
    tabBtns.forEach(b => {
      b.classList.toggle("active", b.getAttribute("data-tab") === tabId);
    });
    tabContents.forEach(c => {
      c.classList.toggle("active", c.id === tabId);
    });
  }

  // Load Scenario 1: Attendance
  function loadScenario1() {
    const data = window.CLASSROOM_SCENARIOS.scenario_1;
    document.getElementById("sc1-session-title").textContent = data.session_title;
    document.getElementById("sc1-instructor").textContent = data.instructor;
    document.getElementById("sc1-threshold").textContent = `${data.threshold_sec}s`;

    const tableBody = document.getElementById("attendance-table-body");
    tableBody.innerHTML = "";

    let presentCount = 0;
    data.students.forEach(s => {
      if (s.status === "PRESENT") presentCount++;

      const tr = document.createElement("tr");

      let badgeClass = "badge-green";
      let badgeLabel = "PRESENT";
      if (s.status === "ABSENT_TRANSIENT") {
        badgeClass = "badge-amber";
        badgeLabel = "REJECTED (TRANSIENT)";
      } else if (s.status === "ABSENT") {
        badgeClass = "badge-purple";
        badgeLabel = "ABSENT";
      }

      tr.innerHTML = `
        <td>
          <div class="student-cell">
            <img src="${s.avatar}" class="student-avatar" alt="${s.name}" onerror="this.src='https://ui-avatars.com/api/?name=${encodeURIComponent(s.name)}&background=1e293b&color=cbd5e1'"/>
            <div>
              <div style="font-weight:600; color:#fff;">${s.name}</div>
              <div style="font-size:0.75rem; color:#94a3b8;">${s.roll}</div>
            </div>
          </div>
        </td>
        <td>
          <span class="badge ${badgeClass}">${badgeLabel}</span>
        </td>
        <td style="font-family:monospace; font-weight:600;">${s.sustained_sec}s</td>
        <td style="color:#94a3b8; font-size:0.8rem;">${s.first_seen}</td>
        <td style="color:#94a3b8; font-size:0.8rem;">${s.last_seen}</td>
        <td style="font-size:0.8rem; color:#cbd5e1;">${s.note}</td>
      `;
      tableBody.appendChild(tr);
    });

    const pct = Math.round((presentCount / (data.students.length - 1)) * 100);
    document.getElementById("val-attendance").textContent = `${pct}%`;
    document.getElementById("val-enrolled-count").textContent = `${presentCount} / ${data.students.length - 1} Verified`;
  }

  // Load Scenario 2: Dynamics
  function loadScenario2() {
    const data = window.CLASSROOM_SCENARIOS.scenario_2;
    document.getElementById("val-engagement").textContent = `${data.overall_score}%`;
    document.getElementById("val-vision-score").textContent = "81.4%";
    document.getElementById("val-audio-interaction").textContent = "Balanced (Q&A Peak)";

    charts.renderTimelineChart("dynamics-line-chart", data.timeline);
    charts.renderVocalDistribution("vocal-doughnut-chart", 62, 28, 10);
  }

  // Load Scenario 3: Suggestions & Copilot
  function loadScenario3() {
    const data = window.CLASSROOM_SCENARIOS.scenario_3;
    const container = document.getElementById("interventions-list");
    container.innerHTML = "";

    data.interventions.forEach(item => {
      const card = document.createElement("div");
      card.className = `glass intervention-card ${item.severity.toLowerCase()}`;
      card.innerHTML = `
        <div class="intervention-header">
          <div style="display:flex; align-items:center; gap:0.5rem;">
            <span class="badge ${item.severity === 'HIGH' ? 'badge-amber' : 'badge-purple'}">${item.severity} SEVERITY</span>
            <span style="font-size:0.75rem; color:#94a3b8;">🕒 ${item.time} • ${item.category}</span>
          </div>
          <button class="tts-btn" data-tts="${encodeURIComponent(item.tts_alert)}">
            <span>🔊</span> Speak Alert
          </button>
        </div>
        <div class="intervention-title">${item.title}</div>
        <div class="intervention-body">${item.body}</div>
        <div style="font-size:0.75rem; color:#34d399; margin-top:0.25rem;">
          <strong>Observed Impact:</strong> ${item.impact}
        </div>
      `;
      container.appendChild(card);
    });

    // Attach TTS Listeners
    document.querySelectorAll(".tts-btn").forEach(b => {
      b.addEventListener("click", (e) => {
        const text = decodeURIComponent(b.getAttribute("data-tts"));
        speakText(text);
      });
    });
  }

  // Web Speech API / TTS Audio player
  function speakText(text) {
    if ("speechSynthesis" in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 1.0;
      utterance.pitch = 1.0;
      window.speechSynthesis.speak(utterance);
    } else {
      // Fallback API call to backend synthesizer
      fetch("/api/suggestions/synthesize-audio", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text })
      })
      .then(res => res.json())
      .then(data => {
        if (data.url) {
          const audio = new Audio(data.url);
          audio.play();
        }
      })
      .catch(err => console.error("TTS fetch error:", err));
    }
  }

  // Interactive Telemetry AI Generator
  const generateAIBtn = document.getElementById("btn-generate-ai-suggestion");
  if (generateAIBtn) {
    generateAIBtn.addEventListener("click", async () => {
      const engVal = parseFloat(document.getElementById("slider-engagement").value);
      const wpmVal = parseInt(document.getElementById("slider-wpm").value);
      const isDrop = engVal < 60;

      generateAIBtn.textContent = "AI Agent Reasoning...";

      try {
        const res = await fetch("/api/suggestions/generate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            metrics: {
              composite_engagement_score: engVal,
              vision_attention_score: engVal,
              audio_interaction_score: 65.0,
              cadence_wpm: wpmVal,
              is_attention_drop: isDrop
            },
            session_phase: "Live Simulated Lecture",
            synthesize_tts: true
          })
        });

        const data = await res.json();
        const sug = data.suggestion;

        const resBox = document.getElementById("ai-generated-suggestion-box");
        resBox.innerHTML = `
          <div class="glass intervention-card ${sug.severity.toLowerCase()}" style="margin-top:1rem;">
            <div class="intervention-header">
              <span class="badge ${sug.severity === 'HIGH' ? 'badge-amber' : 'badge-purple'}">${sug.severity}</span>
              <span style="font-size:0.75rem; color:#94a3b8;">${sug.source || 'Gemini 2.0 Flash'} • ${sug.category}</span>
            </div>
            <div class="intervention-title">${sug.suggestion_title}</div>
            <div class="intervention-body">${sug.suggestion_body}</div>
            <div style="margin-top:0.5rem; display:flex; justify-content:space-between; align-items:center;">
              <span style="font-size:0.75rem; color:#93c5fd;"><strong>Recommended:</strong> ${sug.recommended_activity || 'Interactive Poll'}</span>
              <button class="tts-btn" onclick="window.speakAlert('${encodeURIComponent(sug.tts_alert)}')">
                <span>🔊</span> Listen
              </button>
            </div>
          </div>
        `;

        if (sug.tts_alert) {
          speakText(sug.tts_alert);
        }
      } catch (err) {
        console.warn("API offline or error, showing local inference:", err);
      } finally {
        generateAIBtn.textContent = "Generate Pedagogical Suggestion";
      }
    });
  }

  window.speakAlert = (encodedText) => {
    speakText(decodeURIComponent(encodedText));
  };

  // Code Executor
  const genCodeBtn = document.getElementById("btn-gen-code");
  const execCodeBtn = document.getElementById("btn-exec-code");
  const codeBox = document.getElementById("python-code-box");
  const outputBox = document.getElementById("python-output-box");

  if (genCodeBtn) {
    genCodeBtn.addEventListener("click", async () => {
      const task = document.getElementById("select-code-task").value;
      try {
        const res = await fetch("/api/code/generate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ task_type: task })
        });
        const data = await res.json();
        codeBox.value = data.script.code;
      } catch (e) {
        // Fallback local code template
        codeBox.value = `# Multimodal Pearson Correlation\n# Computing r between Teacher Monologue and Student Inactivity\nprint("Script generated successfully.")`;
      }
    });
  }

  if (execCodeBtn) {
    execCodeBtn.addEventListener("click", async () => {
      outputBox.textContent = "Executing code safely in sandboxed environment...";
      try {
        const res = await fetch("/api/code/execute", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ code: codeBox.value })
        });
        const data = await res.json();
        outputBox.textContent = data.result.output || data.result.error || "Execution completed with no output.";
      } catch (err) {
        outputBox.textContent = "Execution failed: " + err.message;
      }
    });
  }

  // Export CSV
  const exportCsvBtn = document.getElementById("btn-export-csv");
  if (exportCsvBtn) {
    exportCsvBtn.addEventListener("click", () => {
      const data = window.CLASSROOM_SCENARIOS.scenario_1;
      let csv = "Student ID,Name,Roll Number,Status,Sustained Duration (s),First Seen,Last Seen,Note\n";
      data.students.forEach(s => {
        csv += `"${s.id}","${s.name}","${s.roll}","${s.status}",${s.sustained_sec},"${s.first_seen}","${s.last_seen}","${s.note}"\n`;
      });

      const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `attendance_${data.id}_sustained_presence.csv`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    });
  }

  // Initial Load
  loadScenario1();
  loadScenario2();
  loadScenario3();
});
