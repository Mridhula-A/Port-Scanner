
const scanForm = document.getElementById("scanForm");
const scanButton = document.getElementById("scanButton");

let pollingInterval = null;


// =====================================
// STAGE 9.1 - START SCAN
// =====================================

scanForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const target = document.getElementById("target").value.trim();
    const startPort = Number(document.getElementById("startPort").value);
    const endPort = Number(document.getElementById("endPort").value);
    const authorized = document.getElementById("authorized").checked;

    if (!authorized) {
        alert("Please confirm that you have permission to scan this system.");
        return;
    }

    if (
        !Number.isInteger(startPort) ||
        !Number.isInteger(endPort) ||
        startPort < 1 ||
        endPort > 65535 ||
        endPort < 1 ||
        startPort > endPort
    ) {
        alert("Please enter a valid port range (1–65535).");
        return;
    }

    if (endPort - startPort + 1 > 1000) {
        alert("For this educational version, scan a maximum of 1000 ports at a time.");
        return;
    }

    if (pollingInterval) {
        clearInterval(pollingInterval);
        pollingInterval = null;
    }

    resetDashboard();

    scanButton.disabled = true;
    scanButton.textContent = "Starting Scan...";

    try {

        const response = await fetch("/api/scan", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                target: target,
                start_port: startPort,
                end_port: endPort,
                authorized: authorized
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Unable to start scan.");
        }

        document.getElementById("scanStatus").textContent = "Scanning";
        scanButton.textContent = "Scanning...";

        pollingInterval = setInterval(checkScanStatus, 700);

        checkScanStatus();

    } catch (error) {

        alert(error.message);

        scanButton.disabled = false;
        scanButton.textContent = "Start Scanning →";

        document.getElementById("scanStatus").textContent = "Error";
    }
});


// =====================================
// STAGE 9.1 - CHECK SCAN PROGRESS
// =====================================

async function checkScanStatus() {

    try {

        const response = await fetch("/api/status");

        if (!response.ok) {
            throw new Error("Could not retrieve scan status.");
        }

        const data = await response.json();

        document.getElementById("totalScanned").textContent = data.completed || 0;
        document.getElementById("openPorts").textContent = data.open_count || 0;
        document.getElementById("closedPorts").textContent = data.closed_count || 0;

        const progress = data.total > 0
            ? Math.round((data.completed / data.total) * 100)
            : 0;

        document.getElementById("progressText").textContent = progress + "%";
        document.getElementById("progressFill").style.width = progress + "%";

        displayResults(data.results || []);

        if (data.error) {
            throw new Error(data.error);
        }

        // SCAN COMPLETED

        if (!data.running && data.completed > 0) {

            clearInterval(pollingInterval);
            pollingInterval = null;

            document.getElementById("scanStatus").textContent = "Completed";

            scanButton.disabled = false;
            scanButton.textContent = "Start New Scan →";

            // STAGE 9.2 - DOWNLOAD REPORT

            const reportMessage = document.getElementById("reportMessage");

            reportMessage.replaceChildren();

            if (data.report) {

                reportMessage.append("Report saved: ");

                const link = document.createElement("a");

                link.href = `/download/${encodeURIComponent(data.report)}`;
                link.textContent = "Download Scan Report";

                reportMessage.appendChild(link);

            } else {

                reportMessage.textContent = "Scan completed.";

            }

            // Refresh history after a completed scan
            loadScanHistory();

        } else if (!data.running && data.completed === 0) {

            clearInterval(pollingInterval);
            pollingInterval = null;

            document.getElementById("scanStatus").textContent = "Ready";

            scanButton.disabled = false;
            scanButton.textContent = "Start Scanning →";
        }

    } catch (error) {

        clearInterval(pollingInterval);
        pollingInterval = null;

        document.getElementById("scanStatus").textContent = "Error";

        scanButton.disabled = false;
        scanButton.textContent = "Start Scanning →";

        alert(error.message);
    }
}


// =====================================
// STAGE 9.4 - DISPLAY RESULTS WITH STATUS LABELS
// =====================================

function displayResults(results) {

    const resultsBody = document.getElementById("resultsBody");

    if (results.length === 0) {

        resultsBody.innerHTML = `
            <tr>
                <td colspan="3" class="empty-state">
                    Waiting for scan results...
                </td>
            </tr>
        `;

        return;
    }

    resultsBody.replaceChildren();

    results
        .slice()
        .sort((a, b) => a[0] - b[0])
        .forEach(result => {

            const [port, status, service] = result;

            const row = document.createElement("tr");

            // PORT
            const portCell = document.createElement("td");
            portCell.textContent = port;

            // SERVICE
            const serviceCell = document.createElement("td");
            serviceCell.textContent = service;

            // STATUS
            const statusCell = document.createElement("td");

            const statusBadge = document.createElement("span");

            statusBadge.textContent = status;

            if (status === "OPEN") {

                statusBadge.className = "status-open";

            } else if (status === "CLOSED / NO CONNECTION") {

                statusBadge.className = "status-closed";

            } else {

                statusBadge.className = "status-error";

            }

            statusCell.appendChild(statusBadge);

            row.append(portCell, serviceCell, statusCell);

            resultsBody.appendChild(row);

        });
}


// =====================================
// RESET DASHBOARD
// =====================================

function resetDashboard() {

    document.getElementById("totalScanned").textContent = "0";
    document.getElementById("openPorts").textContent = "0";
    document.getElementById("closedPorts").textContent = "0";

    document.getElementById("progressText").textContent = "0%";
    document.getElementById("progressFill").style.width = "0%";

    document.getElementById("scanStatus").textContent = "Starting";
    document.getElementById("reportMessage").textContent = "";

    document.getElementById("resultsBody").innerHTML = `
        <tr>
            <td colspan="3" class="empty-state">
                Preparing your scan...
            </td>
        </tr>
    `;
}


// =====================================
// STAGE 9.3 - LOAD SCAN HISTORY
// =====================================

async function loadScanHistory() {

    const historyBody = document.getElementById("historyBody");

    historyBody.replaceChildren();

    const loadingRow = document.createElement("tr");
    const loadingCell = document.createElement("td");

    loadingCell.colSpan = 4;
    loadingCell.className = "empty-state";
    loadingCell.textContent = "Loading scan history...";

    loadingRow.appendChild(loadingCell);
    historyBody.appendChild(loadingRow);

    try {

        const response = await fetch("/api/history");

        if (!response.ok) {
            throw new Error("Unable to load scan history.");
        }

        const data = await response.json();

        historyBody.replaceChildren();

        if (!data.reports || data.reports.length === 0) {

            const row = document.createElement("tr");
            const cell = document.createElement("td");

            cell.colSpan = 4;
            cell.className = "empty-state";
            cell.textContent = "No previous scan reports found.";

            row.appendChild(cell);
            historyBody.appendChild(row);

            return;
        }

        data.reports.forEach(report => {

            const row = document.createElement("tr");

            const targetCell = document.createElement("td");
            targetCell.textContent = report.target;

            const dateCell = document.createElement("td");
            dateCell.textContent = report.date;

            const reportCell = document.createElement("td");
            reportCell.textContent = report.filename;

            const actionCell = document.createElement("td");

            const downloadLink = document.createElement("a");

            downloadLink.href =
                `/download/${encodeURIComponent(report.filename)}`;

            downloadLink.textContent = "Download";
            downloadLink.className = "history-download";

            actionCell.appendChild(downloadLink);

            row.append(
                targetCell,
                dateCell,
                reportCell,
                actionCell
            );

            historyBody.appendChild(row);

        });

    } catch (error) {

        historyBody.replaceChildren();

        const row = document.createElement("tr");
        const cell = document.createElement("td");

        cell.colSpan = 4;
        cell.className = "empty-state";
        cell.textContent = error.message;

        row.appendChild(cell);
        historyBody.appendChild(row);

    }
}


// =====================================
// REFRESH HISTORY BUTTON
// =====================================

document.getElementById("refreshHistory").addEventListener(
    "click",
    loadScanHistory
);


// =====================================
// LOAD HISTORY WHEN WEBSITE OPENS
// =====================================

loadScanHistory();
