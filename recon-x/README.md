# RECON-X 🔍

A modular, zero-dependency cybersecurity reconnaissance toolkit for Linux.  
Pure Python 3 — no pip installs required to run.

```
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗      ██╗  ██╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║      ╚██╗██╔╝
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║█████╗ ╚███╔╝
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║╚════╝ ██╔██╗
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║      ██╔╝ ██╗
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝      ╚═╝  ╚═╝
```

---

## Project Structure

```
recon-x/
├── main.py                  # Entry point & menu loop
├── requirements.txt
├── README.md
├── core/
│   ├── __init__.py
│   ├── config.py            # Colors, constants, menu palette
│   └── base.py              # BaseModule abstract class
├── modules/
│   ├── __init__.py          # Module registry (ALL_MODULES list)
│   ├── ip_lookup.py         # [01] IP Geo-location
│   ├── domain_lookup.py     # [02] WHOIS
│   ├── port_scanner.py      # [03] Threaded TCP scanner
│   ├── dns_lookup.py        # [04] DNS records (A, MX, TXT, …)
│   ├── osint_search.py      # [05] OSINT dork URL generator
│   ├── system_info.py       # [06] Local system info
│   ├── ping_test.py         # [07] ICMP ping with stats
│   ├── header_grabber.py    # [08] HTTP header inspector
│   ├── ssl_checker.py       # [09] TLS/SSL certificate audit
│   ├── subdomain_finder.py  # [10] DNS brute-force subdomains
│   ├── username_search.py   # [11] Username presence on 20+ platforms
│   └── dir_bruteforce.py    # [12] HTTP directory discovery
└── utils/
    ├── __init__.py
    └── helpers.py           # Shared utilities (banner, menu, net helpers)
```

---

## Quick Start

```bash
# Clone / copy the project
cd recon-x

# Ensure system tools are available
sudo apt install whois dnsutils   # Debian/Ubuntu

# Run
python3 main.py
```

---

## Example Usage

### 1 · IP Lookup
```
[IP or hostname] ▶ 8.8.8.8

  IP                    8.8.8.8
  Country               United States
  Region                California
  City                  Mountain View
  ISP                   Google LLC
  Org                   Google LLC
```

### 3 · Port Scanner
```
[IP or hostname] ▶ scanme.nmap.org
[Scan mode]      ▶ 1              (top ports)
[Timeout]        ▶ 0.5

  PORT     STATE     SERVICE
  ─────────────────────────────────────
  22/tcp   open      SSH
  80/tcp   open      HTTP
```

### 9 · SSL Checker
```
[domain] ▶ github.com

  Common Name           github.com
  Issuer Org            DigiCert Inc
  Valid Until           2026-03-26
  ✔  Valid for 330 more days
  TLS Version           TLSv1.3
  Cipher Suite          TLS_AES_128_GCM_SHA256
```

### 11 · Username Search
```
[username] ▶ torvalds

  ✔ GitHub          https://github.com/torvalds
  ✔ Reddit          https://www.reddit.com/user/torvalds/
  ...
  ✔ Found on 3 / 20 platforms.
```

### 12 · Directory Bruteforce
```
[URL] ▶ https://example.com

  [200]  https://example.com/robots.txt
  [403]  https://example.com/admin
  [301]  https://example.com/login
```

---

## Adding a New Module

1. Create `modules/my_module.py`:

```python
from core.base import BaseModule
from core.config import C
from utils.helpers import pause

class MyModule(BaseModule):
    NAME  = "My Module"
    COLOR = C.CYAN
    DESC  = "Does something useful"

    def run(self) -> None:
        self.header()
        target = self.prompt("Enter target", self.COLOR)
        # ... your logic ...
        self.ok("Done!")
        pause()
```

2. Register it in `modules/__init__.py`:

```python
from modules.my_module import MyModule
ALL_MODULES = [..., MyModule]
```

3. Add a menu entry in `utils/helpers.py` → `MENU_ITEMS` and a color in `core/config.py` → `MENU_COLORS`.

---

## System Dependencies

| Tool    | Used by          | Install                        |
|---------|------------------|--------------------------------|
| `whois` | Domain Lookup    | `sudo apt install whois`       |
| `dig`   | DNS Lookup       | `sudo apt install dnsutils`    |
| `ping`  | Ping Test        | pre-installed                  |
| `ip`    | System Info      | pre-installed (iproute2)       |
| `free`  | System Info      | pre-installed (procps)         |

---

## Legal Notice

RECON-X is intended for **authorized security testing and educational use only**.  
Always obtain explicit permission before scanning or probing systems you do not own.
