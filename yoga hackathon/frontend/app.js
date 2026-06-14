const uploadZone = document.getElementById("uploadZone");
const browseButton = document.getElementById("browseButton");
const fileInput = document.getElementById("fileInput");
const statusCard = document.getElementById("statusCard");
const statusLine = document.getElementById("statusLine");
const progressFill = document.getElementById("progressFill");
const dashboardSection = document.getElementById("dashboardSection");
const emptyState = document.getElementById("emptyState");
const dashboardContent = document.getElementById("dashboardContent");
const profileCard = document.getElementById("profileCard");
const summaryCard = document.getElementById("summaryCard");
const medicationsCard = document.getElementById("medicationsCard");
const riskCard = document.getElementById("riskCard");
const labsCard = document.getElementById("labsCard");
const riskChart = document.getElementById("riskChart");
const labsChart = document.getElementById("labsChart");
const chatQuestion = document.getElementById("chatQuestion");
const chatSubmit = document.getElementById("chatSubmit");
const chatResponse = document.getElementById("chatResponse");
const toggleTheme = document.getElementById("toggleTheme");
const navLinks = document.querySelectorAll(".nav-link");
const heroSection = document.getElementById("heroSection");
const uploadPanel = document.getElementById("uploadPanel");
const chatPanel = document.getElementById("chatPanel");

let currentPatientId = null;

const steps = [
  "Scanning Document...",
  "Extracting Medical Entities...",
  "Running Risk Analysis...",
  "Generating Summary...",
  "Building Dashboard...",
];

function setStatus(text, percent = 0) {
  statusLine.textContent = text;
  progressFill.style.width = `${percent}%`;
}

function showStatus() {
  statusCard.hidden = false;
  setStatus("Preparing upload...");
}

function hideStatus() {
  statusCard.hidden = true;
  progressFill.style.width = "0";
}

function updateStep(index) {
  setStatus(steps[index] || "Processing...");
  progressFill.style.width = `${20 + index * 16}%`;
}

function showDashboard() {
  emptyState.hidden = true;
  dashboardContent.hidden = false;
}

function resetDashboard() {
  emptyState.hidden = false;
  dashboardContent.hidden = true;
}

function renderProfile(patient) {
  profileCard.innerHTML = `
    <h3>Patient Profile</h3>
    <div class="profile-grid">
      <p><strong>Name</strong><br>${patient.name || "N/A"}</p>
      <p><strong>Age</strong><br>${patient.age || "N/A"}</p>
      <p><strong>Gender</strong><br>${patient.gender || "N/A"}</p>
      <p><strong>Blood Group</strong><br>${patient.blood_group || "N/A"}</p>
      <p><strong>Diagnosis</strong><br>${patient.diagnosis || patient.disease || "N/A"}</p>
    </div>
  `;
}

function renderSummary(summary) {
  summaryCard.innerHTML = `
    <h3>AI Summary</h3>
    <p>${summary || "No summary available."}</p>
  `;
}

function renderMedications(medications) {
  medicationsCard.innerHTML = `<h3>Medication Plan</h3>`;
  if (!medications || medications.length === 0) {
    medicationsCard.innerHTML += `<p>No medications extracted from the document.</p>`;
    return;
  }
  const rows = medications.map((item) => `
    <tr>
      <td>${item.drug_name || "-"}</td>
      <td>${item.dosage || "-"}</td>
      <td>${item.frequency || "-"}</td>
      <td>${item.duration || "-"}</td>
    </tr>
  `).join("");
  medicationsCard.innerHTML += `
    <div class="table-responsive">
      <table>
        <thead><tr><th>Drug</th><th>Dosage</th><th>Frequency</th><th>Duration</th></tr></thead>
        <tbody>${rows}</tbody>
      </table>
    </div>
  `;
}

function severityClass(severity) {
  if (!severity) return "green";
  const key = severity.toLowerCase();
  if (key.includes("dark")) return "dark-red";
  if (key.includes("red")) return "red";
  if (key.includes("orange")) return "orange";
  return "green";
}

function renderRisks(risks) {
  riskCard.innerHTML = `<h3>Risk Alerts</h3>`;
  if (!risks || risks.length === 0) {
    riskCard.innerHTML += `<p>No risk alerts were generated from the analysis.</p>`;
    return;
  }
  const list = risks.map((item) => `
    <div class="risk-pill ${severityClass(item.severity)}">
      <strong>${item.title}</strong>
      <p>${item.description || "No details available."}</p>
      <span>Severity: ${item.severity}</span>
    </div>
  `).join("");
  riskCard.innerHTML += `<div class="risk-list">${list}</div>`;
}

function renderLabs(patient) {
  labsCard.innerHTML = `<h3>Lab Results</h3>`;
  const rows = [
    ["Hemoglobin", patient.hemoglobin],
    ["WBC", patient.wbc],
    ["RBC", patient.rbc],
    ["Platelets", patient.platelets],
    ["Glucose", patient.glucose],
    ["Cholesterol", patient.cholesterol],
  ]
    .filter((item) => item[1])
    .map((item) => `
      <tr>
        <td>${item[0]}</td>
        <td>${item[1]}</td>
      </tr>
    `).join("");
  labsCard.innerHTML += rows ? `
    <div class="table-responsive">
      <table>
        <thead><tr><th>Lab</th><th>Value</th></tr></thead>
        <tbody>${rows}</tbody>
      </table>
    </div>
  ` : `<p>No lab values were extracted.</p>`;
}

function plotRiskChart(risks) {
  const labels = risks.map((item) => item.title);
  const values = risks.map((_, index) => 1);
  if (!labels.length) {
    riskChart.innerHTML = `<h3>Risk Severity</h3><p>No risk data available for plotting.</p>`;
    return;
  }
  const colors = risks.map((item) => {
    const key = item.severity.toLowerCase();
    if (key.includes("dark")) return "#991b1b";
    if (key.includes("red")) return "#ef4444";
    if (key.includes("orange")) return "#f97316";
    return "#22c55e";
  });
  Plotly.newPlot(riskChart, [{
    values,
    labels,
    type: "pie",
    marker: { colors },
    hole: 0.6,
  }], {
    title: "Risk Severity",
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    font: { color: "#f8fafc" },
  }, {responsive: true});
}

function plotLabsChart(patient) {
  const labels = ["Hemoglobin", "WBC", "RBC", "Platelets", "Glucose", "Cholesterol"];
  const values = [patient.hemoglobin, patient.wbc, patient.rbc, patient.platelets, patient.glucose, patient.cholesterol]
    .map((value) => (value ? Number(value.replace(/[^0-9.]/g, "")) : 0));
  const nonZeroValues = labels.filter((_, index) => values[index] > 0);
  const nonZeroNumbers = values.filter((value) => value > 0);
  if (!nonZeroNumbers.length) {
    labsChart.innerHTML = `<h3>Lab Trends</h3><p>No numeric lab data available for charting.</p>`;
    return;
  }
  Plotly.newPlot(labsChart, [{
    x: nonZeroValues,
    y: nonZeroNumbers,
    type: "bar",
    marker: { color: "#38bdf8" },
  }], {
    title: "Lab Result Trends",
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    font: { color: "#f8fafc" },
  }, {responsive: true});
}

function renderDashboard(data) {
  if (!data || !data.patient) return;
  currentPatientId = data.patient.id;
  renderProfile(data.patient);
  renderSummary(data.summary);
  renderMedications(data.medications);
  renderRisks(data.risks);
  renderLabs(data.patient);
  plotRiskChart(data.risks);
  plotLabsChart(data.patient);
  showDashboard();
}

async function uploadDocument(file) {
  showStatus();
  setTimeout(() => updateStep(0), 100);
  const form = new FormData();
  form.append("file", file);
  try {
    setTimeout(() => updateStep(1), 800);
    const response = await fetch("/upload", { method: "POST", body: form });
    setTimeout(() => updateStep(2), 1600);
    const payload = await response.json();
    if (!response.ok) {
      statusLine.textContent = payload.detail || "Upload failed. Please try another file.";
      return;
    }
    setTimeout(() => updateStep(3), 2400);
    renderDashboard(payload);
    setTimeout(() => updateStep(4), 3200);
    setTimeout(() => hideStatus(), 800);
  } catch (error) {
    statusLine.textContent = "Upload failed due to network or processing error.";
  }
}

uploadZone.addEventListener("click", () => fileInput.click());
browseButton.addEventListener("click", () => fileInput.click());
fileInput.addEventListener("change", (event) => {
  const file = event.target.files[0];
  if (file) {
    uploadDocument(file);
  }
});

uploadZone.addEventListener("dragover", (event) => {
  event.preventDefault();
  uploadZone.classList.add("dragover");
});

uploadZone.addEventListener("dragleave", () => {
  uploadZone.classList.remove("dragover");
});

uploadZone.addEventListener("drop", (event) => {
  event.preventDefault();
  uploadZone.classList.remove("dragover");
  const file = event.dataTransfer.files[0];
  if (file) {
    uploadDocument(file);
  }
});

chatSubmit.addEventListener("click", async () => {
  const question = chatQuestion.value.trim();
  if (!question || !currentPatientId) {
    chatResponse.textContent = "Upload a document first and ask a question about the extracted record.";
    return;
  }
  chatResponse.textContent = "Analyzing your question...";
  const response = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ patient_id: currentPatientId, question }),
  });
  const payload = await response.json();
  chatResponse.textContent = payload.answer || "No answer could be generated.";
});

toggleTheme.addEventListener("click", () => {
  document.body.classList.toggle("light-mode");
});

navLinks.forEach((button) => {
  button.addEventListener("click", () => {
    navLinks.forEach((link) => link.classList.remove("active"));
    button.classList.add("active");
    const target = button.dataset.target;
    heroSection.scrollIntoView({ behavior: "smooth" });
    if (target === "upload") uploadPanel.scrollIntoView({ behavior: "smooth" });
    if (target === "chat") chatPanel.scrollIntoView({ behavior: "smooth" });
  });
});
