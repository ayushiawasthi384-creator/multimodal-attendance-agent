/**
 * Live Classroom Vision & Audio Telemetry Processor
 * Uses WebRTC getUserMedia, Web Audio API Analyzer, and Canvas Rendering
 */

class ClassroomStudio {
  constructor(videoElement, canvasElement, audioCanvasElement) {
    this.video = videoElement;
    this.canvas = canvasElement;
    this.audioCanvas = audioCanvasElement;
    this.stream = null;
    this.audioCtx = null;
    this.analyzer = null;
    this.dataArray = null;
    this.isCameraActive = false;
    this.isSimulating = true;
    this.simulatedFaces = [
      { id: "Aarav S.", x: 0.15, y: 0.25, w: 0.18, h: 0.35, yaw: 3.2, pitch: -2.1, status: "ATTENTIVE", color: "#10B981" },
      { id: "Beatriz S.", x: 0.42, y: 0.22, w: 0.17, h: 0.34, yaw: -6.5, pitch: -4.0, status: "ATTENTIVE", color: "#10B981" },
      { id: "Chen W.", x: 0.68, y: 0.28, w: 0.19, h: 0.36, yaw: 1.0, pitch: 1.2, status: "ATTENTIVE", color: "#10B981" },
      { id: "Guest (Passerby)", x: 0.88, y: 0.35, w: 0.10, h: 0.25, yaw: 45.0, pitch: 0.0, status: "TRANSIENT", color: "#EF4444" }
    ];
    this.animationId = null;
  }

  async startCamera() {
    try {
      this.stream = await navigator.mediaDevices.getUserMedia({
        video: { width: 1280, height: 720 },
        audio: true
      });
      this.video.srcObject = this.stream;
      await this.video.play();
      this.isCameraActive = true;
      this.isSimulating = false;

      // Start Audio Analyzer
      this.setupAudioAnalyzer(this.stream);
      return { success: true };
    } catch (err) {
      console.warn("Camera/Mic access denied or unavailable, continuing in CCTV simulation mode:", err);
      this.isCameraActive = false;
      this.isSimulating = true;
      return { success: false, error: err.message };
    }
  }

  stopCamera() {
    if (this.stream) {
      this.stream.getTracks().forEach(t => t.stop());
      this.stream = null;
    }
    this.isCameraActive = false;
    this.isSimulating = true;
    if (this.audioCtx) {
      this.audioCtx.close();
      this.audioCtx = null;
    }
  }

  setupAudioAnalyzer(stream) {
    try {
      window.AudioContext = window.AudioContext || window.webkitAudioContext;
      this.audioCtx = new AudioContext();
      const source = this.audioCtx.createMediaStreamSource(stream);
      this.analyzer = this.audioCtx.createAnalyser();
      this.analyzer.fftSize = 64;
      source.connect(this.analyzer);
      const bufferLength = this.analyzer.frequencyBinCount;
      this.dataArray = new Uint8Array(bufferLength);
    } catch (e) {
      console.warn("Audio Context init failed:", e);
    }
  }

  startRenderLoop(onTelemetryUpdate) {
    const ctx = this.canvas.getContext("2d");
    const audioCtx2D = this.audioCanvas ? this.audioCanvas.getContext("2d") : null;

    let tick = 0;

    const render = () => {
      tick++;
      const w = this.canvas.width = this.canvas.clientWidth;
      const h = this.canvas.height = this.canvas.clientHeight;

      ctx.clearRect(0, 0, w, h);

      // If simulated mode, draw simulated classroom environment backdrop
      if (this.isSimulating) {
        ctx.fillStyle = "#0c1222";
        ctx.fillRect(0, 0, w, h);

        // Classroom background grid lines
        ctx.strokeStyle = "rgba(255, 255, 255, 0.05)";
        ctx.lineWidth = 1;
        for (let x = 0; x < w; x += 40) {
          ctx.beginPath();
          ctx.moveTo(x, 0);
          ctx.lineTo(x, h);
          ctx.stroke();
        }

        // Live Feed Badge
        ctx.fillStyle = "rgba(16, 185, 129, 0.2)";
        ctx.strokeStyle = "#10B981";
        ctx.strokeRect(15, 15, 140, 26);
        ctx.fillRect(15, 15, 140, 26);
        ctx.fillStyle = "#10B981";
        ctx.font = "bold 11px system-ui";
        ctx.fillText("● AI CCTV SIMULATOR", 25, 32);

        // Render participant bounding boxes with subtle sinusoidal micro-movements
        this.simulatedFaces.forEach((face, idx) => {
          const sway = Math.sin(tick * 0.05 + idx) * 0.008;
          const fx = (face.x + sway) * w;
          const fy = face.y * h;
          const fw = face.w * w;
          const fh = face.h * h;

          // Bounding Box
          ctx.strokeStyle = face.color;
          ctx.lineWidth = 2;
          ctx.strokeRect(fx, fy, fw, fh);

          // Header Tag
          ctx.fillStyle = face.color;
          ctx.fillRect(fx, fy - 20, fw, 20);
          ctx.fillStyle = "#ffffff";
          ctx.font = "bold 11px system-ui";
          ctx.fillText(`${face.id} [${face.status}]`, fx + 5, fy - 6);

          // Head Pose Telemetry Badge below
          ctx.fillStyle = "rgba(0,0,0,0.7)";
          ctx.fillRect(fx, fy + fh + 4, fw, 34);
          ctx.fillStyle = "#cbd5e1";
          ctx.font = "10px monospace";
          ctx.fillText(`Yaw: ${(face.yaw + Math.sin(tick * 0.03) * 2).toFixed(1)}°`, fx + 4, fy + fh + 16);
          ctx.fillText(`Pitch: ${(face.pitch + Math.cos(tick * 0.02)).toFixed(1)}°`, fx + 4, fy + fh + 29);
        });
      } else {
        // Live camera is active: draw facial landmark simulation on live user feed
        const cx = w * 0.35;
        const cy = h * 0.25;
        const cw = w * 0.3;
        const ch = h * 0.5;

        ctx.strokeStyle = "#38bdf8";
        ctx.lineWidth = 2;
        ctx.strokeRect(cx, cy, cw, ch);

        ctx.fillStyle = "#38bdf8";
        ctx.fillRect(cx, cy - 22, cw, 22);
        ctx.fillStyle = "#000000";
        ctx.font = "bold 12px system-ui";
        ctx.fillText("LIVE PARTICIPANT • SUSTAINED PRESENT", cx + 8, cy - 6);

        // Corner brackets
        const bLen = 20;
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 3;
        ctx.beginPath();
        // Top-left
        ctx.moveTo(cx, cy + bLen); ctx.lineTo(cx, cy); ctx.lineTo(cx + bLen, cy);
        // Top-right
        ctx.moveTo(cx + cw - bLen, cy); ctx.lineTo(cx + cw, cy); ctx.lineTo(cx + cw, cy + bLen);
        // Bottom-left
        ctx.moveTo(cx, cy + ch - bLen); ctx.lineTo(cx, cy + ch); ctx.lineTo(cx + bLen, cy + ch);
        // Bottom-right
        ctx.moveTo(cx + cw - bLen, cy + ch); ctx.lineTo(cx + cw, cy + ch); ctx.lineTo(cx + cw, cy + ch - bLen);
        ctx.stroke();
      }

      // Audio Spectrum Visualization
      if (audioCtx2D) {
        const aw = this.audioCanvas.width = this.audioCanvas.clientWidth;
        const ah = this.audioCanvas.height = this.audioCanvas.clientHeight;
        audioCtx2D.clearRect(0, 0, aw, ah);

        if (this.analyzer && this.dataArray) {
          this.analyzer.getByteFrequencyData(this.dataArray);
          const barWidth = (aw / this.dataArray.length) * 1.5;
          let bx = 0;
          for (let i = 0; i < this.dataArray.length; i++) {
            const barHeight = (this.dataArray[i] / 255) * ah;
            audioCtx2D.fillStyle = `hsl(${210 + i * 4}, 90%, 55%)`;
            audioCtx2D.fillRect(bx, ah - barHeight, barWidth - 2, barHeight);
            bx += barWidth;
          }
        } else {
          // Synthetic ambient classroom waveform animation
          const barCount = 28;
          const barW = aw / barCount;
          for (let i = 0; i < barCount; i++) {
            const hVal = Math.sin(tick * 0.1 + i * 0.4) * 0.35 + 0.45;
            const barH = hVal * (ah * 0.7);
            audioCtx2D.fillStyle = i % 2 === 0 ? "#3b82f6" : "#8b5cf6";
            audioCtx2D.fillRect(i * barW, ah - barH, barW - 3, barH);
          }
        }
      }

      this.animationId = requestAnimationFrame(render);
    };

    render();
  }
}

window.ClassroomStudio = ClassroomStudio;
