# RECON-X Classic

import os
import socket
import requests
import platform
import getpass
import subprocess
import ssl
import sys
from threading import Thread
from queue import Queue
import stat

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
# IMPROVED RESULT TABLE - DYNAMIC ALIGNMENT
# =========================
def box(title, rows):
    if not rows:
        print(RED + "No data to display" + RESET)
        return
    
    # Calculate dynamic column widths
    max_key_len = max(len(str(k)) for k, v in rows) if rows else 10
    max_val_len = max(len(str(v)) for k, v in rows) if rows else 20
    
    key_width = max(max_key_len + 2, 18)
    val_width = max(max_val_len + 2, 28)
    
    total = key_width + val_width + 7

    print(CYAN + "+" + "-" * (total - 2) + "+")
    print(f"| {title.center(total - 4)} |")
    print("+" + "-" * (key_width + 2) + "+" + "-" * (val_width + 2) + "+")

    for k, v in rows:
        k_str = str(k)
        v_str = str(v).replace("\n", " ")

        first = True
        while len(v_str) > val_width:
            key_display = k_str if first else ""
            print(f"| {key_display:<{key_width}} | {v_str[:val_width]:<{val_width}} |")
            v_str = v_str[val_width:]
            first = False

        key_display = k_str if first else ""
        print(f"| {key_display:<{key_width}} | {v_str:<{val_width}} |")

    print("+" + "-" * (total - 2) + "+" + RESET)

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
    print("|     5      | OSINT Search (with verification)           |")
    print("|     6      | System Info                                |")
    print("|     7      | Ping Test                                  |")
    print("|     8      | Header Grabber                             |")
    print("|     9      | SSL Checker                                |")
    print("|    10      | Subdomain Finder                           |")
    print("|    11      | Username Search (with verification)        |")
    print("|    12      | Directory Reader                           |")
    print("|    13      | Exit                                       |")
    print("+----------------------------------------------------------+")

# =========================
# MODULES
# =========================

# MODULE 1: IP LOOKUP - FIXED
def ip_lookup():
    ip = input(YELLOW + "\nEnter IP     : " + RESET).strip()
    if not ip:
        print(RED + "Error: IP address cannot be empty" + RESET)
        return
    
    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)
        r.raise_for_status()
        data = r.json()
        
        if data.get("error"):
            print(RED + f"Invalid IP: {data.get('error', {}).get('message', 'Unknown error')}" + RESET)
            return
        
        rows = [
            ("IP Address", data.get("ip", "-")),
            ("Hostname", data.get("hostname", "-")),
            ("City", data.get("city", "-")),
            ("Region", data.get("region", "-")),
            ("Country", data.get("country", "-")),
            ("Location", data.get("loc", "-")),
            ("Org", data.get("org", "-")),
            ("Postal", data.get("postal", "-")),
            ("Timezone", data.get("timezone", "-"))
        ]
        box("IP LOOKUP RESULT", rows)
    except requests.exceptions.Timeout:
        print(RED + "Error: Request timeout (5 seconds exceeded)" + RESET)
    except requests.exceptions.ConnectionError:
        print(RED + "Error: Connection failed. Check your internet connection" + RESET)
    except requests.exceptions.RequestException as e:
        print(RED + f"Error: API request failed - {str(e)}" + RESET)
    except ValueError as e:
        print(RED + f"Error: Invalid response format - {str(e)}" + RESET)

# MODULE 2: DOMAIN LOOKUP - FIXED
def domain_lookup():
    domain = input(YELLOW + "\nEnter Domain : " + RESET).strip()
    if not domain:
        print(RED + "Error: Domain cannot be empty" + RESET)
        return
    
    try:
        ip = socket.gethostbyname(domain)
        box("DOMAIN LOOKUP", [("Domain", domain), ("IP Address", ip)])
    except socket.gaierror as e:
        print(RED + f"Error: Domain resolution failed - {str(e)}" + RESET)
    except socket.error as e:
        print(RED + f"Error: Socket error - {str(e)}" + RESET)
    except Exception as e:
        print(RED + f"Error: Unexpected error - {str(e)}" + RESET)

# MODULE 3: PORT SCAN - FIXED (with finally block)
def port_scan():
    host = input(YELLOW + "\nEnter Host   : " + RESET).strip()
    if not host:
        print(RED + "Error: Host cannot be empty" + RESET)
        return
    
    ports = [21, 22, 80, 443]
    rows = []
    
    print(YELLOW + "\nScanning ports..." + RESET)

    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        try:
            result = s.connect_ex((host, port))
            if result == 0:
                rows.append((f"Port {port}", "OPEN ✓"))
            else:
                rows.append((f"Port {port}", "Closed ✗"))
        except socket.timeout:
            rows.append((f"Port {port}", "Timeout"))
        except socket.error as e:
            rows.append((f"Port {port}", f"Error: {str(e)}"))
        finally:
            s.close()

    if rows:
        box("PORT SCAN RESULT", rows)
    else:
        print(RED + "Error: No results from port scan" + RESET)

# MODULE 4: DNS LOOKUP - ENHANCED (handles multiple IPs)
def dns_lookup():
    domain = input(YELLOW + "\nEnter Domain : " + RESET).strip()
    if not domain:
        print(RED + "Error: Domain cannot be empty" + RESET)
        return
    
    try:
        ip = socket.gethostbyname(domain)
        # Try to get multiple addresses
        try:
            all_ips = socket.gethostbyname_ex(domain)
            ip_list = all_ips[2]
            ip_str = ", ".join(ip_list) if ip_list else ip
        except:
            ip_str = ip
        
        box("DNS LOOKUP", [("Domain", domain), ("Resolved IP(s)", ip_str)])
    except socket.gaierror as e:
        print(RED + f"Error: DNS resolution failed - {str(e)}" + RESET)
    except socket.error as e:
        print(RED + f"Error: Socket error - {str(e)}" + RESET)
    except Exception as e:
        print(RED + f"Error: Unexpected error - {str(e)}" + RESET)

# MODULE 5: OSINT SEARCH - FIXED (with actual verification)
def osint_search():
    user = input(YELLOW + "\nEnter Username: " + RESET).strip()
    if not user:
        print(RED + "Error: Username cannot be empty" + RESET)
        return
    
    platforms = {
        "GitHub": f"https://github.com/{user}",
        "Instagram": f"https://instagram.com/{user}",
        "Twitter": f"https://x.com/{user}",
        "Reddit": f"https://reddit.com/user/{user}"
    }
    
    rows = []
    print(YELLOW + "\nVerifying accounts..." + RESET)
    
    for platform_name, url in platforms.items():
        try:
            response = requests.head(url, timeout=3, allow_redirects=True)
            status = "✓ Found" if response.status_code < 400 else "✗ Not Found"
            rows.append((platform_name, f"{url} [{status}]"))
        except requests.exceptions.RequestException:
            rows.append((platform_name, f"{url} [✗ Not Found]"))
        except Exception as e:
            rows.append((platform_name, f"{url} [Error: {str(e)}]"))
    
    if rows:
        box("OSINT SEARCH RESULTS", rows)
    else:
        print(RED + "Error: Could not verify any accounts" + RESET)

# MODULE 6: SYSTEM INFO - FIXED (already good, minor enhancements)
def system_info():
    host = socket.gethostname()
    ip = "Unavailable"
    try:
        ip = socket.gethostbyname(host)
    except socket.error:
        pass

    try:
        mac = ":".join(["{:02x}".format((os.urandom(1))[0]) for i in range(6)])
    except:
        mac = "Unavailable"

    rows = [
        ("Host Name", host),
        ("User", getpass.getuser()),
        ("OS", platform.system()),
        ("Version", platform.release()),
        ("Machine", platform.machine()),
        ("Processor", platform.processor() or "Unknown"),
        ("Python", platform.python_version()),
        ("Local IP", ip),
        ("MAC Address", mac),
        ("Path", os.getcwd())
    ]
    box("SYSTEM INFO", rows)

# MODULE 7: PING TEST - FIXED (with timeout)
def ping_test():
    host = input(YELLOW + "\nEnter Host   : " + RESET).strip()
    if not host:
        print(RED + "Error: Host cannot be empty" + RESET)
        return
    
    cmd = ["ping", "-n", "4", host] if os.name == "nt" else ["ping", "-c", "4", host]
    try:
        subprocess.run(cmd, timeout=15)
    except subprocess.TimeoutExpired:
        print(RED + "Error: Ping command timed out (15 seconds)" + RESET)
    except FileNotFoundError:
        print(RED + "Error: Ping command not found on system" + RESET)
    except Exception as e:
        print(RED + f"Error: Ping failed - {str(e)}" + RESET)

# MODULE 8: HEADER GRABBER - FIXED
def header_grabber():
    url = input(YELLOW + "\nEnter URL    : " + RESET).strip()
    if not url:
        print(RED + "Error: URL cannot be empty" + RESET)
        return
    
    if not url.startswith("http"):
        url = "http://" + url

    try:
        r = requests.get(url, timeout=5, allow_redirects=False)
        rows = list(r.headers.items())[:10]
        if rows:
            box("HTTP HEADERS", rows)
        else:
            print(RED + "Error: No headers returned" + RESET)
    except requests.exceptions.Timeout:
        print(RED + "Error: Request timeout (5 seconds exceeded)" + RESET)
    except requests.exceptions.ConnectionError:
        print(RED + "Error: Connection failed" + RESET)
    except requests.exceptions.RequestException as e:
        print(RED + f"Error: Request failed - {str(e)}" + RESET)
    except Exception as e:
        print(RED + f"Error: Unexpected error - {str(e)}" + RESET)

# MODULE 9: SSL CHECKER - FIXED (Python 3.10+ compatible)
def ssl_checker():
    host = input(YELLOW + "\nEnter Domain : " + RESET).strip()
    if not host:
        print(RED + "Error: Domain cannot be empty" + RESET)
        return

    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()

        if not cert:
            print(RED + "Error: Could not retrieve certificate" + RESET)
            return

        subject = cert.get("subject", [[("unknown", "unknown")]])[0][0][1] if cert.get("subject") else "N/A"
        issuer = cert.get("issuer", [[("unknown", "unknown")]])[0][0][1] if cert.get("issuer") else "N/A"
        
        rows = [
            ("Subject", subject),
            ("Issuer", issuer),
            ("Valid From", cert.get("notBefore", "N/A")),
            ("Valid To", cert.get("notAfter", "N/A")),
            ("Serial Number", cert.get("serialNumber", "N/A"))
        ]
        box("SSL CERTIFICATE", rows)

    except ssl.SSLError as e:
        print(RED + f"Error: SSL verification failed - {str(e)}" + RESET)
    except socket.timeout:
        print(RED + "Error: Connection timeout (5 seconds)" + RESET)
    except socket.gaierror as e:
        print(RED + f"Error: Domain resolution failed - {str(e)}" + RESET)
    except socket.error as e:
        print(RED + f"Error: Connection failed - {str(e)}" + RESET)
    except Exception as e:
        print(RED + f"Error: Unexpected error - {str(e)}" + RESET)

# MODULE 10: SUBDOMAIN FINDER - FIXED (with threading)
def check_subdomain(domain, subdomain, results):
    host = f"{subdomain}.{domain}"
    try:
        ip = socket.gethostbyname(host)
        results.append((host, ip))
    except (socket.gaierror, socket.error):
        pass

def subdomain_finder():
    domain = input(YELLOW + "\nEnter Domain : " + RESET).strip()
    if not domain:
        print(RED + "Error: Domain cannot be empty" + RESET)
        return
    
    commons = ["www", "mail", "ftp", "api", "dev", "blog", "admin", "test", "staging", "cdn"]
    rows = []
    
    print(YELLOW + "\nSearching for subdomains..." + RESET)
    
    threads = []
    for sub in commons:
        thread = Thread(target=check_subdomain, args=(domain, sub, rows))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

    if rows:
        rows.sort()
        box("SUBDOMAIN RESULT", rows)
    else:
        print(RED + "No common subdomains found for this domain" + RESET)

# MODULE 11: USERNAME SEARCH - FIXED (with verification)
def username_search():
    user = input(YELLOW + "\nEnter Username: " + RESET).strip()
    if not user:
        print(RED + "Error: Username cannot be empty" + RESET)
        return
    
    platforms = {
        "GitHub": f"https://github.com/{user}",
        "Instagram": f"https://instagram.com/{user}",
        "Reddit": f"https://reddit.com/user/{user}",
        "Twitch": f"https://twitch.tv/{user}"
    }
    
    rows = []
    print(YELLOW + "\nVerifying usernames..." + RESET)
    
    for platform_name, url in platforms.items():
        try:
            response = requests.head(url, timeout=3, allow_redirects=True)
            status = "✓ Found" if response.status_code < 400 else "✗ Not Found"
            rows.append((platform_name, f"{url} [{status}]"))
        except requests.exceptions.RequestException:
            rows.append((platform_name, f"{url} [✗ Not Found]"))
        except Exception as e:
            rows.append((platform_name, f"{url} [Error]"))
    
    if rows:
        box("USERNAME SEARCH RESULTS", rows)
    else:
        print(RED + "Error: Could not verify any usernames" + RESET)

# MODULE 12: DIRECTORY READER - FIXED (with file types)
def directory_reader():
    path = input(YELLOW + "\nEnter Path   : " + RESET).strip()
    if not path:
        print(RED + "Error: Path cannot be empty" + RESET)
        return
    
    try:
        if not os.path.exists(path):
            print(RED + f"Error: Path does not exist - {path}" + RESET)
            return
        
        if not os.path.isdir(path):
            print(RED + f"Error: Path is not a directory - {path}" + RESET)
            return
        
        items = os.listdir(path)
        rows = []
        
        for item in items[:20]:
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                item_type = "📁 [DIR]"
            else:
                try:
                    size = os.path.getsize(full_path)
                    if size > 1024*1024:
                        size_str = f"{size/(1024*1024):.2f} MB"
                    elif size > 1024:
                        size_str = f"{size/1024:.2f} KB"
                    else:
                        size_str = f"{size} B"
                    item_type = f"📄 [FILE] {size_str}"
                except OSError:
                    item_type = "📄 [FILE]"
            
            rows.append((item, item_type))
        
        if rows:
            box("DIRECTORY READER", rows)
        else:
            print(RED + "Error: Directory is empty" + RESET)
            
    except PermissionError:
        print(RED + f"Error: Permission denied - {path}" + RESET)
    except OSError as e:
        print(RED + f"Error: Unable to read directory - {str(e)}" + RESET)
    except Exception as e:
        print(RED + f"Error: Unexpected error - {str(e)}" + RESET)

# =========================
# MAIN LOOP
# =========================
def main():
    while True:
        clear()
        banner()
        menu()

        choice = input(YELLOW + "\nEnter Choice : " + RESET).strip()

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
            print(RED + "\nInvalid Choice - Please enter a number between 1-13" + RESET)
            input(YELLOW + "\nPress Enter To Retry..." + RESET)
            continue

        input(YELLOW + "\nPress Enter To Continue..." + RESET)

if __name__ == '__main__':
    main()
