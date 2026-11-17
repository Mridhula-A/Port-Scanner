
# ==================================
# PORT SCANNER PROJECT
# ==================================

from scanner import scan_range

print("================================")
print("          PORT SCANNER")
print("================================")

print("Developed by: Mridhula A")

print("================================")

# Get target IP
target = input("\nEnter Target IP Address: ")

# Get port range
start_port = int(input("Enter Starting Port: "))

end_port = int(input("Enter Ending Port: "))

# Validate port range
if not (1 <= start_port <= end_port <= 65535):
    print("\nInvalid Port Range!")
    print("Ports must be between 1 and 65535.")
    exit()

if end_port - start_port + 1 > 1000:
    print("\nMaximum 1000 ports allowed per scan.")
    exit()

# Start scanning
print("\n================================")
print("         SCAN STARTED")
print("================================")

print("Target:", target)
print("Port Range:", start_port, "-", end_port)

scan_range(target, start_port, end_port)

print("\n================================")
print("         SCAN COMPLETED")
print("================================")
