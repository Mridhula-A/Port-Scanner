
# ==================================
# PORT SCANNER - SERVICE DATABASE
# ==================================

# Common port-to-service mappings

SERVICES = {

    20: "FTP Data",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    67: "DHCP",
    68: "DHCP",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "Remote Desktop",
    5432: "PostgreSQL",
    8080: "HTTP Alternate",
    8443: "HTTPS Alternate"

}


# ==================================
# SERVICE IDENTIFICATION FUNCTION
# ==================================

def get_service(port):

    return SERVICES.get(port, "Unknown Service")
