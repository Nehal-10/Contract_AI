const API = "http://127.0.0.1:8000";

let riskChart = null;
let typeChart = null;

/* ==========================
   EVENTS
========================== */
document.getElementById("analyzeBtn").addEventListener("click", analyzeContract);

/* ==========================
   INITIAL LOAD
========================== */
loadHistory();

/* ==========================
   ANALYZE CONTRACT
========================== */
async function analyzeContract() {
    console.log("Analyze button clicked");
    const file = document.getElementById("pdfFile").files[0];

    if (!file) {
        alert("Please select a PDF file.");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    document.getElementById("loader").classList.remove("hidden");

    try {
        const response = await fetch(`${API}/analyze`, {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        console.log("API Data received:", data);

        showResults(data);
        loadHistory();

    } catch (error) {
        console.error("Analysis Error:", error);
        alert("Analysis failed.");
    } finally {
        document.getElementById("loader").classList.add("hidden");
    }
}

/* ==========================
   RESULTS
========================== */
function showResults(data) {
    console.log("Rendering results...", data);

    // Populate Text Blocks
    document.getElementById("contractType").textContent = data.contract_type || "NDA";
    document.getElementById("riskScore").textContent = data.risk_score !== undefined ? data.risk_score : "0";
    
    const riskLevelElement = document.getElementById("riskLevel");
    const riskLevel = data.risk_level || "LOW";
    riskLevelElement.textContent = riskLevel;
    riskLevelElement.className = `result-box ${riskLevel.toLowerCase()}`;

    document.getElementById("summary").textContent = data.summary || "No summary provided.";

    // Render Sub-sections Safely
    showRisks(data.risks || []);
    showCompliance(data.compliance_details || []);
    drawCharts(data);
}

/* ==========================
   RISKS
========================== */
function showRisks(risks) {
    const container = document.getElementById("riskContainer");
    container.innerHTML = "";

    if (!risks || risks.length === 0) {
        container.innerHTML = `<p>No risks detected.</p>`;
        return;
    }

    risks.forEach(risk => {
        container.innerHTML += `
            <div class="risk-card">
                <h4>${risk.risk_type || "Finding"}</h4>
                <p><strong>Severity:</strong> ${risk.severity || "N/A"}</p>
                <p>${risk.recommendation || ""}</p>
            </div>`;
    });
}

/* ==========================
   COMPLIANCE
========================== */
function showCompliance(items) {
    const table = document.getElementById("complianceTable");
    table.innerHTML = "";

    if (!items || items.length === 0) {
        table.innerHTML = `<tr><td colspan="2">No compliance details found.</td></tr>`;
        return;
    }

    items.forEach(item => {
        const statusText = item.status || "UNKNOWN";
        const statusClass = statusText.toUpperCase() === "FOUND" ? "found" : "missing";

        table.innerHTML += `
            <tr>
                <td>${item.requirement}</td>
                <td class="${statusClass}">${statusText}</td>
            </tr>`;
    });
}

/* ==========================
   HISTORY
========================== */
async function loadHistory() {
    try {
        const response = await fetch(`${API}/history`);
        const data = await response.json();
        const table = document.getElementById("historyTable");
        table.innerHTML = "";

        data.forEach(item => {
            table.innerHTML += `
                <tr>
                    <td>${item.filename}</td>
                    <td>${item.contract_type}</td>
                    <td>${item.risk_score}</td>
                    <td>${item.created_at || "Just now"}</td>
                </tr>`;
        });
    } catch (error) {
        console.error("History Error:", error);
    }
}

/* ==========================
   CHARTS
========================== */
function drawCharts(data) {
    try {
        if (riskChart) riskChart.destroy();
        if (typeChart) typeChart.destroy();

        const riskCtx = document.getElementById("riskChart");
        const typeCtx = document.getElementById("typeChart");

        if (riskCtx) {
            riskChart = new Chart(riskCtx, {
                type: "bar",
                data: {
                    labels: ["Risk Score"],
                    datasets: [{
                        label: "Score Metric",
                        data: [data.risk_score || 0],
                        backgroundColor: ["#e74c3c"]
                    }]
                },
                options: { responsive: true }
            });
        }

        if (typeCtx) {
            typeChart = new Chart(typeCtx, {
                type: "pie",
                data: {
                    labels: [data.contract_type || "NDA"],
                    datasets: [{
                        data: [1],
                        backgroundColor: ["#3498db"]
                    }]
                },
                options: { responsive: true }
            });
        }
    } catch (chartError) {
        console.error("Chart rendering skipped safely:", chartError);
    }
}
