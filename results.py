
# ==================================
# PORT SCANNER - RESULT MANAGEMENT
# ==================================

import os
from datetime import datetime


# ==================================
# SAVE SCAN RESULTS
# ==================================

def save_results(target, start_port, end_port, results):

    # Create scans folder if it doesn't exist
    os.makedirs("scans", exist_ok=True)

    # Get current date and time
    scan_time = datetime.now()

    timestamp = scan_time.strftime("%Y%m%d_%H%M%S")

    # Generate report filename
    filename = f"scan_report_{timestamp}.txt"

    filepath = os.path.join("scans", filename)

    # Calculate scan statistics
    total_ports = len(results)

    open_ports = sum(
        1 for result in results
        if result[1] == "OPEN"
    )

    closed_ports = sum(
        1 for result in results
        if result[1] == "CLOSED / NO CONNECTION"
    )

    error_ports = total_ports - open_ports - closed_ports

    # Write report
    with open(filepath, "w", encoding="utf-8") as file:

        file.write("====================================\n")
        file.write("          PORT SCAN REPORT\n")
        file.write("====================================\n\n")

        file.write(f"Target IP: {target}\n")

        file.write(
            f"Scan Date: {scan_time.strftime('%d-%m-%Y')}\n"
        )

        file.write(
            f"Scan Time: {scan_time.strftime('%H:%M:%S')}\n"
        )

        file.write(
            f"Port Range: {start_port} - {end_port}\n\n"
        )

        file.write("------------------------------------\n")
        file.write("           SCAN RESULTS\n")
        file.write("------------------------------------\n\n")

        for port, status, service in sorted(results):

            file.write(
                f"[{status}] Port {port} - {service}\n"
            )

        file.write("\n------------------------------------\n")
        file.write("           SCAN SUMMARY\n")
        file.write("------------------------------------\n\n")

        file.write(f"Total Ports Scanned: {total_ports}\n")
        file.write(f"Open Ports: {open_ports}\n")
        file.write(f"Closed Ports: {closed_ports}\n")
        file.write(f"Error Ports: {error_ports}\n")

        file.write("\n====================================\n")
        file.write("           END OF REPORT\n")
        file.write("====================================\n")

    print("\nScan report saved successfully!")
    print("Report Location:", filepath)
    return filepath