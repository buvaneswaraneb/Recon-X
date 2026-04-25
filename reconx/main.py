# RECON-X Classic

import os
import socket
import requests
import platform
import getpass
import subprocess
import ssl

# =========================
# COLORS
# =========================
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

# =========================
# CLEAR
# =========================
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# =========================
# BANNER
# =========================
def banner():
    print(CYAN + r"""
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗      ██╗  ██╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║      ╚██╗██╔╝
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║█████╗ ╚███╔╝
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║╚════╝ ██╔██╗
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║      ██╔╝ ██╗
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝      ╚═╝  ╚═╝
""" + RESET)

    print(GREEN + "+----------------------------------------------------------+")
    print("|                  Linux Recon Toolkit                     |")
    print("|              kernel linked | stealth ready               |")
    print("+----------------------------------------------------------+")
    print("| ports primed | osint live | dns loaded | recon mode      |")
    print("+----------------------------------------------------------+" + RESET)

# =========================
# OLD STYLE RESULT TABLE
# =========================
def box(title, rows):
    total = 58
    left = 20
    right = total - left - 3

    print(CYAN + "+" + "-" * total + "+")
    print(f"| {title.center(total - 2)} |")
    print("+" + "-" * (left + 2) + "+" + "-" * (right + 2) + "+")

    for k, v in rows:
        k = str(k)
        v = str(v).replace("\n", " ")

        first = True
        while len(v) > right:
            key = k if first else ""
            print(f"| {key:<{left}} | {v[:right]:<{right}} |")
            v = v[right:]
            first = False

        key = k if first else ""
        print(f"| {key:<{left}} | {v:<{right}} |")

    print("+" + "-" * total + "+" + RESET)

# =========================
# MENU
# =========================
def menu():
    print(YELLOW + "\n                 >>> Enter The Grid <<<\n" + RESET)

    print("+----------------------------------------------------------+")
    print("| OPTION NO. | FEATURES                                   |")
    print("+----------------------------------------------------------+")
    print("|     1      | IP Lookup                                  |")
    print("|     2      | Domain Lookup                              |")
    print("|     3      | Port Scan                                  |")
    print("|     4      | DNS Lookup                                 |")
    print("|     5      | OSINT Search                               |")
    print("|     6      | System Info                                |")
    print("|     7      | Ping Test                                  |")
    print("|     8      | Header Grabber                             |")
    print("|     9      | SSL Checker                                |")
    print("|    10      | Subdomain Finder                           |")
    print("|    11      | Username Search                            |")
    print("|    12      | Directory Reader                           |")
    print("|    13      | Exit                                       |")
    print("+----------------------------------------------------------+")

# =========================
# MODULES
# =========================
def ip_lookup():
    ip = input(YELLOW + "\nEnter IP     : " + RESET)
    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5).json()
        rows = [
            ("IP Address", r.get("ip", "-")),
            ("Hostname", r.get("hostname", "-")),
            ("City", r.get("city", "-")),
            ("Region", r.get("region", "-")),
            ("Country", r.get("country", "-")),
            ("Location", r.get("loc", "-")),
            ("Org", r.get("org", "-")),
            ("Postal", r.get("postal", "-")),
            ("Timezone", r.get("timezone", "-"))
        ]
        box("IP LOOKUP RESULT", rows)
    except:
        print(RED + "Lookup Failed" + RESET)

def domain_lookup():
    domain = input(YELLOW + "\nEnter Domain : " + RESET)
    try:
        ip = socket.gethostbyname(domain)
        box("DOMAIN LOOKUP", [("Domain", domain), ("IP Address", ip)])
    except:
        print(RED + "Lookup Failed" + RESET)

def port_scan():
    host = input(YELLOW + "\nEnter Host   : " + RESET)
    ports = [21, 22, 80, 443]
    rows = []

    for port in ports:
        s = socket.socket()
        s.settimeout(0.7)
        try:
            s.connect((host, port))
            rows.append((f"Port {port}", "OPEN"))
        except:
            rows.append((f"Port {port}", "Closed"))
        s.close()

    box("PORT SCAN RESULT", rows)

def dns_lookup():
    domain = input(YELLOW + "\nEnter Domain : " + RESET)
    try:
        ip = socket.gethostbyname(domain)
        box("DNS LOOKUP", [("Domain", domain), ("Resolved IP", ip)])
    except:
        print(RED + "DNS Failed" + RESET)

def osint_search():
    user = input(YELLOW + "\nEnter Username: " + RESET)
    rows = [
        ("GitHub", f"github.com/{user}"),
        ("Instagram", f"instagram.com/{user}"),
        ("Twitter", f"x.com/{user}"),
        ("Reddit", f"reddit.com/user/{user}")
    ]
    box("OSINT SEARCH", rows)

def system_info():
    host = socket.gethostname()
    try:
        ip = socket.gethostbyname(host)
    except:
        ip = "Unavailable"

    rows = [
        ("Host Name", host),
        ("User", getpass.getuser()),
        ("OS", platform.system()),
        ("Version", platform.release()),
        ("Machine", platform.machine()),
        ("Processor", platform.processor()),
        ("Python", platform.python_version()),
        ("Local IP", ip),
        ("Path", os.getcwd())
    ]
    box("SYSTEM INFO", rows)

def ping_test():
    host = input(YELLOW + "\nEnter Host   : " + RESET)
    cmd = ["ping", "-n", "4", host] if os.name == "nt" else ["ping", "-c", "4", host]
    subprocess.run(cmd)

def header_grabber():
    url = input(YELLOW + "\nEnter URL    : " + RESET)
    if not url.startswith("http"):
        url = "http://" + url

    try:
        r = requests.get(url, timeout=5)
        rows = list(r.headers.items())[:10]
        box("HTTP HEADERS", rows)
    except:
        print(RED + "Header Fetch Failed" + RESET)

def ssl_checker():
    host = input(YELLOW + "\nEnter Domain : " + RESET)

    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=host) as s:
            s.settimeout(5)
            s.connect((host, 443))
            cert = s.getpeercert()

        rows = [
            ("Subject", cert["subject"][0][0][1]),
            ("Issuer", cert["issuer"][0][0][1]),
            ("Valid From", cert["notBefore"]),
            ("Valid To", cert["notAfter"])
        ]
        box("SSL CERTIFICATE", rows)

    except:
        print(RED + "SSL Check Failed" + RESET)

def subdomain_finder():
    domain = input(YELLOW + "\nEnter Domain : " + RESET)
    commons = ["www", "mail", "ftp", "api", "dev", "blog"]
    rows = []

    for sub in commons:
        host = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(host)
            rows.append((host, ip))
        except:
            pass

    if rows:
        box("SUBDOMAIN RESULT", rows)
    else:
        print(RED + "No Common Subdomains Found" + RESET)

def username_search():
    user = input(YELLOW + "\nEnter Username: " + RESET)
    rows = [
        ("GitHub", f"github.com/{user}"),
        ("Instagram", f"instagram.com/{user}"),
        ("Reddit", f"reddit.com/user/{user}"),
        ("Twitch", f"twitch.tv/{user}")
    ]
    box("USERNAME SEARCH", rows)

def directory_reader():
    path = input(YELLOW + "\nEnter Path   : " + RESET)
    try:
        items = os.listdir(path)
        rows = [("Item", item) for item in items[:15]]
        box("DIRECTORY READER", rows)
    except:
        print(RED + "Unable To Read Directory" + RESET)

# =========================
# MAIN LOOP
# =========================
def main():
    while True:
        clear()
        banner()
        menu()

        choice = input(YELLOW + "\nEnter Choice : " + RESET)

        if choice == "1":
            ip_lookup()
        elif choice == "2":
            domain_lookup()
        elif choice == "3":
            port_scan()
        elif choice == "4":
            dns_lookup()
        elif choice == "5":
            osint_search()
        elif choice == "6":
            system_info()
        elif choice == "7":
            ping_test()
        elif choice == "8":
            header_grabber()
        elif choice == "9":
            ssl_checker()
        elif choice == "10":
            subdomain_finder()
        elif choice == "11":
            username_search()
        elif choice == "12":
            directory_reader()
        elif choice == "13":
            print(GREEN + "\nExiting RECON-X...\n" + RESET)
            break
        else:
            print(RED + "\nInvalid Choice" + RESET)
            input(YELLOW + "\nPress Enter To Retry..." + RESET)
            continue

        input(YELLOW + "\nPress Enter To Exit..." + RESET)
        break

if __name__ == "__main__":
    main()
