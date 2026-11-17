
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    send_from_directory,
    abort
)

import ipaddress
import threading
import os
import glob

from concurrent.futures import ThreadPoolExecutor, as_completed

from scanner import scan_port
from results import save_results


app = Flask(__name__)


# =====================================
# SHARED SCAN INFORMATION
# =====================================

scan_state = {
    "running": False,
    "target": None,
    "total": 0,
    "completed": 0,
    "results": [],
    "error": None,
    "report": None
}

state_lock = threading.Lock()


# =====================================
# HOME PAGE
# =====================================

@app.route("/")
def home():
    return render_template("index.html")


# =====================================
# BACKGROUND SCANNING FUNCTION
# =====================================

def run_scan(target, start_port, end_port):

    try:
        results = []

        with ThreadPoolExecutor(max_workers=50) as executor:

            futures = {
                executor.submit(scan_port, target, port): port
                for port in range(start_port, end_port + 1)
            }

            for future in as_completed(futures):

                result = future.result()
                results.append(result)

                with state_lock:
                    scan_state["results"].append(result)
                    scan_state["completed"] += 1

        # Save scan report
        report_path = save_results(
            target,
            start_port,
            end_port,
            results
        )

        # Store report filename
        with state_lock:
            scan_state["report"] = os.path.basename(report_path)

    except Exception as error:

        with state_lock:
            scan_state["error"] = str(error)

    finally:

        with state_lock:
            scan_state["running"] = False


# =====================================
# START SCAN API
# =====================================

@app.route("/api/scan", methods=["POST"])
def start_scan():

    data = request.get_json(silent=True) or {}

    target = data.get("target", "").strip()
    start_port = data.get("start_port")
    end_port = data.get("end_port")
    authorized = data.get("authorized")

    # Permission confirmation
    if authorized is not True:
        return jsonify({
            "error": "Please confirm scan permission."
        }), 400

    # Validate IPv4 address
    try:
        ipaddress.IPv4Address(target)

    except ValueError:
        return jsonify({
            "error": "Enter a valid IPv4 address."
        }), 400

    # Validate port values
    if (
        isinstance(start_port, bool)
        or isinstance(end_port, bool)
        or not isinstance(start_port, int)
        or not isinstance(end_port, int)
    ):
        return jsonify({
            "error": "Port values must be whole numbers."
        }), 400

    # Port range validation
    if not (1 <= start_port <= 65535):
        return jsonify({
            "error": "Invalid starting port."
        }), 400

    if not (1 <= end_port <= 65535):
        return jsonify({
            "error": "Invalid ending port."
        }), 400

    if start_port > end_port:
        return jsonify({
            "error": "Start port cannot exceed end port."
        }), 400

    if end_port - start_port + 1 > 1000:
        return jsonify({
            "error": "Maximum 1000 ports per scan."
        }), 400

    # Prevent multiple simultaneous scans
    with state_lock:

        if scan_state["running"]:
            return jsonify({
                "error": "A scan is already running."
            }), 409

        scan_state.update({
            "running": True,
            "target": target,
            "total": end_port - start_port + 1,
            "completed": 0,
            "results": [],
            "error": None,
            "report": None
        })

    # Launch background thread
    thread = threading.Thread(
        target=run_scan,
        args=(target, start_port, end_port),
        daemon=True
    )

    thread.start()

    return jsonify({
        "message": "Scan started successfully."
    }), 202


# =====================================
# LIVE SCAN STATUS API
# =====================================

@app.route("/api/status")
def scan_status():

    with state_lock:

        results = list(scan_state["results"])

        open_count = sum(
            1 for result in results
            if result[1] == "OPEN"
        )

        closed_count = sum(
            1 for result in results
            if result[1] == "CLOSED / NO CONNECTION"
        )

        return jsonify({
            "running": scan_state["running"],
            "target": scan_state["target"],
            "total": scan_state["total"],
            "completed": scan_state["completed"],
            "open_count": open_count,
            "closed_count": closed_count,
            "results": results,
            "error": scan_state["error"],
            "report": scan_state["report"]
        })


# =====================================
# STAGE 9.3 - SCAN HISTORY API
# =====================================

@app.route("/api/history")
def scan_history():

    scans_folder = os.path.join(
        app.root_path,
        "scans"
    )

    report_files = glob.glob(
        os.path.join(scans_folder, "scan_report_*.txt")
    )

    # Newest reports first
    report_files.sort(
        key=os.path.getmtime,
        reverse=True
    )

    reports = []

    for filepath in report_files:

        filename = os.path.basename(filepath)

        target = "Unknown"
        scan_date = "Unknown"

        try:

            with open(filepath, "r", encoding="utf-8") as file:

                for line in file:

                    if line.startswith("Target IP:"):
                        target = line.split(":", 1)[1].strip()

                    elif line.startswith("Scan Date:"):
                        scan_date = line.split(":", 1)[1].strip()

        except OSError:
            continue

        reports.append({
            "filename": filename,
            "target": target,
            "date": scan_date
        })

    return jsonify({
        "reports": reports
    })


# =====================================
# DOWNLOAD SCAN REPORT
# =====================================

@app.route("/download/<path:filename>")
def download_report(filename):

    # Allow only generated scan report filenames
    if (
        not filename.startswith("scan_report_")
        or not filename.endswith(".txt")
        or "/" in filename
        or "\\" in filename
    ):
        abort(404)

    scans_folder = os.path.join(
        app.root_path,
        "scans"
    )

    return send_from_directory(
        scans_folder,
        filename,
        as_attachment=True
    )


# =====================================
# RUN FLASK WEBSITE
# =====================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        use_reloader=False
    )
