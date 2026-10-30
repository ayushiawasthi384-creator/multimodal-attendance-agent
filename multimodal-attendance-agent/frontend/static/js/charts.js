/**
 * Chart.js Integration for Classroom Intelligence Telemetry
 */

class ClassroomCharts {
  constructor() {
    this.timelineChart = null;
    this.vocalChart = null;
  }

  renderTimelineChart(canvasId, timelineData) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    if (this.timelineChart) {
      this.timelineChart.destroy();
    }

    const labels = timelineData.map(d => `${d.min}m`);
    const engagement = timelineData.map(d => d.fusion);
    const vision = timelineData.map(d => d.vision);
    const monologue = timelineData.map(d => d.monologue);
    const inactivity = timelineData.map(d => d.inactivity);

    this.timelineChart = new Chart(ctx, {
      type: "line",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Composite Engagement Score",
            data: engagement,
            borderColor: "#38bdf8",
            backgroundColor: "rgba(56, 189, 248, 0.15)",
            borderWidth: 3,
            fill: true,
            tension: 0.35,
            pointRadius: 4,
            pointBackgroundColor: "#38bdf8"
          },
          {
            label: "Attentive Head Pose %",
            data: vision,
            borderColor: "#10b981",
            borderWidth: 2,
            borderDash: [4, 4],
            fill: false,
            tension: 0.2,
            pointRadius: 2
          },
          {
            label: "Teacher Monologue %",
            data: monologue,
            borderColor: "#f59e0b",
            borderWidth: 2,
            fill: false,
            tension: 0.2,
            pointRadius: 2
          },
          {
            label: "Student Inactivity %",
            data: inactivity,
            borderColor: "#ef4444",
            borderWidth: 1.5,
            borderDash: [2, 2],
            fill: false,
            tension: 0.2,
            pointRadius: 2
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            labels: { color: "#94a3b8", font: { size: 11 } }
          },
          tooltip: {
            callbacks: {
              footer: (items) => {
                const idx = items[0].dataIndex;
                return `Phase: ${timelineData[idx].phase}`;
              }
            }
          }
        },
        scales: {
          y: {
            min: 0,
            max: 100,
            grid: { color: "rgba(255, 255, 255, 0.06)" },
            ticks: { color: "#64748b" }
          },
          x: {
            grid: { color: "rgba(255, 255, 255, 0.04)" },
            ticks: { color: "#64748b" }
          }
        }
      }
    });
  }

  renderVocalDistribution(canvasId, monologuePct, studentPct, silencePct) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    if (this.vocalChart) {
      this.vocalChart.destroy();
    }

    this.vocalChart = new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: ["Teacher Monologue", "Student Interaction", "Silence / Lull"],
        datasets: [{
          data: [monologuePct, studentPct, silencePct],
          backgroundColor: ["#3b82f6", "#10b981", "#64748b"],
          borderColor: "#0f172a",
          borderWidth: 3
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "bottom",
            labels: { color: "#94a3b8", boxWidth: 12, font: { size: 11 } }
          }
        },
        cutout: "70%"
      }
    });
  }
}

window.ClassroomCharts = ClassroomCharts;
