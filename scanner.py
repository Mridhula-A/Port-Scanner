
# ==================================
# PORT SCANNER - SCANNING ENGINE
# MULTITHREADING + REPORT SAVING
# ==================================

import socket

from concurrent.futures import ThreadPoolExecutor, as_completed

from services import get_service
from results import save_results


# ==================================
# SINGLE PORT SCANNING
# ==================================

def scan_port(target, port):

    service = get_service(port)

    try:

        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as sock:

            sock.settimeout(1)

            result = sock.connect_ex((target, port))

            if result == 0:
                status = "OPEN"
            else:
                status = "CLOSED / NO CONNECTION"

            return port, status, service

    except socket.error:

        return port, "ERROR", service


# ==================================
# MULTITHREADED PORT RANGE SCANNING
# ==================================

def scan_range(target, start_port, end_port):

    print("\nStarting Multithreaded Port Scan...")

    print("--------------------------------")

    results = []

    max_workers = 50

    with ThreadPoolExecutor(max_workers=max_workers) as executor:

        futures = [
            executor.submit(scan_port, target, port)
            for port in range(start_port, end_port + 1)
        ]

        for future in as_completed(futures):

            result = future.result()

            results.append(result)

            port, status, service = result

            print(
                f"[{status}] Port {port} - {service}"
            )

    print("--------------------------------")

    print("Multithreaded Scan Completed!")

    # Save scan report
    save_results(
        target,
        start_port,
        end_port,
        results
    )

    return results
