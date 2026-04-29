# RECON-X 🔍
### Modular Cybersecurity Reconnaissance Toolkit for Linux

```
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗      ██╗  ██╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║      ╚██╗██╔╝
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║█████╗ ╚███╔╝
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║╚════╝ ██╔██╗
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║      ██╔╝ ██╗
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝      ╚═╝  ╚═╝
```

> **Pure Python 3 · Zero pip dependencies · Modular OOP · Color CLI · Linux**

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Running the Toolkit](#running-the-toolkit)
- [Module Usage & Expected Output](#module-usage--expected-output)
  - [01 — IP Lookup](#01--ip-lookup)
  - [02 — Domain Lookup](#02--domain-lookup)
  - [03 — Port Scanner](#03--port-scanner)
  - [04 — DNS Lookup](#04--dns-lookup)
  - [05 — OSINT Search](#05--osint-search)
  - [06 — System Info](#06--system-info)
  - [07 — Ping Test](#07--ping-test)
  - [08 — Header Grabber](#08--header-grabber)
  - [09 — SSL Checker](#09--ssl-checker)
  - [10 — Subdomain Finder](#10--subdomain-finder)
  - [11 — Username Search](#11--username-search)
  - [12 — Directory Bruteforce](#12--directory-bruteforce)
- [Test Cases](#test-cases)
- [Adding a New Module](#adding-a-new-module)
- [Troubleshooting](#troubleshooting)
- [Legal Notice](#legal-notice)

---

## Overview

RECON-X is a terminal-based cybersecurity reconnaissance toolkit that bundles 12 common recon tasks into a single, menu-driven CLI. It is designed for:

- Security researchers doing authorized penetration testing
- Students learning network reconnaissance concepts
- SysAdmins auditing their own infrastructure
- CTF (Capture The Flag) players

Every module follows the same OOP pattern (`BaseModule`), making the toolkit trivially easy to extend. All output is color-coded per module for fast visual scanning. No internet API keys, no pip installs — just Python 3 and a Linux terminal.

---

## Features

| # | Module | Method | Accent Color |
|---|--------|--------|--------------|
| 01 | IP Lookup | HTTP → ip-api.com (no key) | Cyan |
| 02 | Domain Lookup | `whois` system command | Green |
| 03 | Port Scanner | Threaded TCP connect (200 workers) | Yellow |
| 04 | DNS Lookup | `dig` system command | Blue |
| 05 | OSINT Search | URL generator (15 sources) | Magenta |
| 06 | System Info | `platform`, `socket`, `shutil`, `subprocess` | Orange |
| 07 | Ping Test | `ping` system command + latency coloring | Teal |
| 08 | Header Grabber | `urllib` HTTP + security audit | Pink |
| 09 | SSL Checker | `ssl` + `socket` TLS handshake | Lime |
| 10 | Subdomain Finder | Threaded DNS brute-force (200-word list) | Purple |
| 11 | Username Search | Threaded HTTP probe (20 platforms) | Red |
| 12 | Directory Bruteforce | Threaded HTTP path discovery | White |

---

## Project Structure

```
recon-x/
│
├── main.py                      ← Entry point & interactive menu loop
├── requirements.txt             ← Zero pip dependencies (stdlib only)
├── README.md                    ← This file
│
├── core/
│   ├── __init__.py
│   ├── config.py                ← ANSI color palette + per-option menu colors
│   └── base.py                  ← BaseModule abstract class (shared helpers)
│
├── modules/
│   ├── __init__.py              ← ALL_MODULES list (menu order = list order)
│   ├── ip_lookup.py             ← [01] Geo-IP via ip-api.com
│   ├── domain_lookup.py         ← [02] WHOIS
│   ├── port_scanner.py          ← [03] TCP scanner, top ports + custom range
│   ├── dns_lookup.py            ← [04] DNS records via dig
│   ├── osint_search.py          ← [05] OSINT dork URL builder
│   ├── system_info.py           ← [06] Local hardware & network info
│   ├── ping_test.py             ← [07] ICMP ping + latency stats
│   ├── header_grabber.py        ← [08] HTTP headers + security header audit
│   ├── ssl_checker.py           ← [09] TLS cert inspector
│   ├── subdomain_finder.py      ← [10] DNS brute-force enumeration
│   ├── username_search.py       ← [11] 20-platform username probe
│   └── dir_bruteforce.py        ← [12] HTTP directory discovery
│
└── utils/
    ├── __init__.py
    └── helpers.py               ← Banner, menu, run_cmd, resolve_host, etc.
```

---

## Setup & Installation

### System Requirements

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.8+ | No walrus operator or match statements used |
| Linux | Any distro | Tested on Ubuntu 22.04, Kali Linux 2024.1 |
| `whois` | any | Module 02 only |
| `dig` | any | Module 04 only |
| `ping` | pre-installed | Module 07 |
| `ip` | pre-installed | Module 06 — part of iproute2 |
| `free` | pre-installed | Module 06 — part of procps |

### Step 1 — Extract the project

```bash
# From the downloaded zip:
unzip recon-x.zip
cd recon-x

# Or clone from version control:
git clone https://github.com/adithyanks2005/Recon-X.git
cd Recon-X/
python recon-x/main.py (Windows)
python3 recon-x/main.py (Linux/Mac)
```

### Step 2 — Install optional system tools

Modules 01, 03, and 05–12 work with **zero** additional installs.
Modules 02 and 04 each need one system package:

```bash
# Debian / Ubuntu / Kali (most common)
sudo apt update && sudo apt install whois dnsutils -y

# Arch Linux / Manjaro
sudo pacman -S whois bind-tools

# Fedora / RHEL / CentOS
sudo dnf install whois bind-utils

# Verify installation
whois --version
dig -v
```

### Step 3 — Verify Python version

```bash
python3 --version
# Python 3.10.12  ← any 3.8+ is fine
```

### Step 4 — (Optional) Make executable

```bash
chmod +x main.py
# Then you can run it as: ./main.py
```

### Confirming zero pip dependencies

```bash
cat requirements.txt
# All core functionality uses Python 3 stdlib only.
# No third-party packages are required to run the toolkit.
```

---

## Running the Toolkit

```bash
# From the recon-x/ directory:
python3 main.py

# Or if you made it executable:
./main.py
```

> **Important:** Always run from the project root (`recon-x/`), not from a parent directory. Relative imports will fail otherwise.

You will see the banner followed by the color-coded menu:

```
  ──────────────────────────────────────────────
  [ 1]  IP Lookup
  [ 2]  Domain Lookup
  [ 3]  Port Scanner
  [ 4]  DNS Lookup
  [ 5]  OSINT Search
  [ 6]  System Info
  [ 7]  Ping Test
  [ 8]  Header Grabber
  [ 9]  SSL Checker
  [10]  Subdomain Finder
  [11]  Username Search
  [12]  Directory Bruteforce
  [13]  Exit
  ──────────────────────────────────────────────

  recon-x ▶ _
```

Type a number (`1`–`13`) and press **Enter**. Press **Ctrl+C** at any time to interrupt the current module and return to the menu.

---

## Module Usage & Expected Output

---

### 01 — IP Lookup

**What it does:** Sends a request to the free `ip-api.com` API to geo-locate an IP address or hostname. No API key required. Works for public IPs only (private ranges return an error).

**Prompts:**
```
  [Enter IP or hostname] ▶
```

**Example — valid public IP:**
```
  [Enter IP or hostname] ▶ 8.8.8.8
```

**Expected output:**
```
  ──────────────────────────────────────────────────
    ◆ IP Lookup
    Geo-locate any public IP address or hostname
  ──────────────────────────────────────────────────

  ℹ  Querying 8.8.8.8 …

  IP                    8.8.8.8
  Country               United States
  Region                California
  City                  Mountain View
  Zip                   94043
  Latitude              37.4056
  Longitude             -122.0775
  ISP                   Google LLC
  Org                   Google LLC
  AS                    AS15169 Google LLC
```

**Example — hostname (auto-resolved):**
```
  [Enter IP or hostname] ▶ scanme.nmap.org
  ℹ  Querying 45.33.32.156 …
  City                  Fremont
  ISP                   Linode, LLC
```

**Example — invalid host:**
```
  [Enter IP or hostname] ▶ not-a-real-host.xyz
  ✘  Could not resolve 'not-a-real-host.xyz'
```

---

### 02 — Domain Lookup

**What it does:** Runs `whois` on a domain and extracts key registration fields: registrar, creation date, expiry date, name servers, and DNSSEC status.

**Requires:** `sudo apt install whois`

**Prompts:**
```
  [Enter domain (e.g. example.com)] ▶
```

**Example:**
```
  [Enter domain (e.g. example.com)] ▶ github.com
```

**Expected output:**
```
  ──────────────────────────────────────────────────
    ◆ Domain Lookup
    WHOIS information for a domain name
  ──────────────────────────────────────────────────

  ℹ  Running WHOIS for github.com …

  Domain Name           GITHUB.COM
  Registrar             MarkMonitor Inc.
  Creation Date         2007-10-09T18:20:50Z
  Updated Date          2024-09-07T09:16:31Z
  Registry Expiry Date  2026-10-09T18:20:50Z
  Name Server           DNS1.P08.NSONE.NET
  Name Server           DNS2.P08.NSONE.NET
  DNSSEC                unsigned
```

**Example — no WHOIS data:**
```
  [Enter domain] ▶ thisdoesnotexist99999abc.com
  ✘  No WHOIS data returned.
```

---

### 03 — Port Scanner

**What it does:** Multi-threaded TCP connect scan. Scans top common ports (default) or a user-defined range. Up to 200 concurrent threads. Shows port, state, and service name.

**Prompts:**
```
  [Enter IP or hostname]                               ▶
  [Scan [1] Top ports [2] Custom range (default 1)]   ▶
  [Timeout per port in seconds (default 0.5)]          ▶
```

**Example — top ports:**
```
  [Enter IP or hostname] ▶ scanme.nmap.org
  [Scan mode]            ▶ 1
  [Timeout]              ▶ 0.5
```

**Expected output:**
```
  ──────────────────────────────────────────────────
    ◆ Port Scanner
    Threaded TCP connect scanner
  ──────────────────────────────────────────────────

  ℹ  Scanning 45.33.32.156 — 1042 ports (timeout=0.5s) …

  PORT     STATE     SERVICE
  ────────────────────────────────────
  22/tcp   open      SSH
  80/tcp   open      HTTP

  Scanned 1042 ports · 2 open
```

**Example — custom range:**
```
  [Scan mode]  ▶ 2
  [Port range] ▶ 8000-9000

  [8080]  8080/tcp   open   HTTP-Alt
  Scanned 1001 ports · 1 open
```

**Example — no open ports:**
```
  [Enter IP or hostname] ▶ 192.0.2.1
  ⚠  No open ports found.
  Scanned 1042 ports · 0 open
```

---

### 04 — DNS Lookup

**What it does:** Queries DNS records using `dig`. Supports A, AAAA, MX, NS, TXT, CNAME, SOA, PTR — or all types at once.

**Requires:** `sudo apt install dnsutils`

**Prompts:**
```
  [Enter domain or IP]            ▶
  [Record type (default ALL)]     ▶
```

**Example — all records:**
```
  [Enter domain or IP] ▶ google.com
  [Record type]        ▶ ALL
```

**Expected output:**
```
  ──────────────────────────────────────────────────
    ◆ DNS Lookup
    Query DNS records for a domain
  ──────────────────────────────────────────────────

  ── A ──
    142.250.195.78

  ── AAAA ──
    2607:f8b0:4004:c09::64

  ── MX ──
    10 smtp.google.com.

  ── NS ──
    ns1.google.com.
    ns2.google.com.
    ns3.google.com.
    ns4.google.com.

  ── TXT ──
    "v=spf1 include:_spf.google.com ~all"
    "google-site-verification=wD8N7i..."
```

**Example — single type:**
```
  [Record type] ▶ MX

  ── MX ──
    10 smtp.google.com.
```

**Example — non-existent domain:**
```
  [Enter domain] ▶ thisdoesnotexist99999.com
  ⚠  No DNS records found for 'thisdoesnotexist99999.com'
```

---

### 05 — OSINT Search

**What it does:** Generates ready-to-use investigation URLs for 15 OSINT sources including Google dorks, Shodan, Censys, HaveIBeenPwned, VirusTotal, URLScan, Wayback Machine, GitHub code search, and Pastebin.

**Prompts:**
```
  [Enter domain, IP, email, or username] ▶
```

**Example:**
```
  [Enter domain, IP, email, or username] ▶ example.com
```

**Expected output:**
```
  ──────────────────────────────────────────────────
    ◆ OSINT Search
    Generate Google, Shodan, and OSINT dork URLs for a target
  ──────────────────────────────────────────────────

  OSINT URLs for: example.com

  ► Google — site
    https://www.google.com/search?q=site:example.com

  ► Google — inurl
    https://www.google.com/search?q=inurl:example.com

  ► Google — intitle
    https://www.google.com/search?q=intitle:example.com

  ► Google — filetype:pdf
    https://www.google.com/search?q=example.com+filetype:pdf

  ► Shodan
    https://www.shodan.io/search?query=example.com

  ► Censys
    https://search.censys.io/search?resource=hosts&q=example.com

  ► Have I Been Pwned
    https://haveibeenpwned.com/account/example.com

  ► VirusTotal
    https://www.virustotal.com/gui/domain/example.com

  ► URLScan.io
    https://urlscan.io/search/#domain:example.com

  ► Wayback Machine
    https://web.archive.org/web/*/example.com

  ► GitHub Search
    https://github.com/search?q=example.com&type=code

  ℹ  Copy URLs into your browser to investigate.
```

---

### 06 — System Info

**What it does:** Displays local machine information across five sections: OS/Platform, Network interfaces, Disk usage, CPU/Memory, and Uptime. No input required.

**Prompts:** None — runs immediately on selection.

**Expected output:**
```
  ──────────────────────────────────────────────────
    ◆ System Info
    Hardware, OS, network interfaces, and resource usage
  ──────────────────────────────────────────────────

  ── OS / Platform ──
  OS                    Linux
  Release               6.5.0-kali3-amd64
  Version               #1 SMP PREEMPT_DYNAMIC Debian 6.5.3-1kali1
  Machine               x86_64
  Processor             x86_64
  Python                3.11.6
  Hostname              kali-vm

  ── Network ──
  Local IP              192.168.1.42
    eth0                192.168.1.42/24
    lo                  127.0.0.1/8

  ── Disk Usage  ( / ) ──
  Total                 476.9 GB
  Used                  42.1 GB
  Free                  434.8 GB

  ── CPU / Memory ──
  CPU Cores             8
  Mem total             15Gi
  Mem used              3.2Gi
  Mem free              8.4Gi
  Mem available         11Gi

  ── Uptime ──
  Uptime                up 2 hours, 14 minutes
```

---

### 07 — Ping Test

**What it does:** Runs ICMP ping and color-codes each reply by latency — green under 50ms, yellow 50–150ms, red above 150ms. Prints packet loss summary.

**Prompts:**
```
  [Enter IP or hostname]           ▶
  [Packet count (default 4)]       ▶
```

**Example — reachable host:**
```
  [Enter IP or hostname] ▶ 1.1.1.1
  [Packet count]         ▶ 4
```

**Expected output (host up):**
```
  ──────────────────────────────────────────────────
    ◆ Ping Test
    ICMP ping with latency statistics
  ──────────────────────────────────────────────────

  ℹ  Pinging 1.1.1.1 × 4 …

  ● 64 bytes from 1.1.1.1: icmp_seq=1 ttl=55 time=9.42 ms   ← green (< 50ms)
  ● 64 bytes from 1.1.1.1: icmp_seq=2 ttl=55 time=8.88 ms
  ● 64 bytes from 1.1.1.1: icmp_seq=3 ttl=55 time=9.01 ms
  ● 64 bytes from 1.1.1.1: icmp_seq=4 ttl=55 time=9.15 ms

  ℹ  4 packets transmitted, 4 received, 0% packet loss, time 3004ms
  ℹ  rtt min/avg/max/mdev = 8.880/9.115/9.420/0.195 ms
  ✔  Host is up.
```

**Expected output (host unreachable):**
```
  ✘ Request timeout for icmp_seq 1
  ✘ Request timeout for icmp_seq 2

  ℹ  2 packets transmitted, 0 received, 100% packet loss
  ⚠  Host unreachable or packet loss detected.
```

---

### 08 — Header Grabber

**What it does:** Fetches HTTP/S response headers and performs an automated security header audit — listing present headers in green and missing security headers in yellow. Also flags server-revealing headers like `Server` and `X-Powered-By`.

**Prompts:**
```
  [Enter URL (e.g. https://example.com)] ▶
```

**Example:**
```
  [Enter URL] ▶ https://github.com
```

**Expected output:**
```
  ──────────────────────────────────────────────────
    ◆ Header Grabber
    Inspect HTTP response headers and security posture
  ──────────────────────────────────────────────────

  ℹ  Fetching headers from https://github.com …

  HTTP 200  https://github.com/

  ── All Headers ──
  Content-Type              text/html; charset=utf-8
  Server                    GitHub.com                  ← orange (interesting)
  Strict-Transport-Security  max-age=31536000; includeSubdomains  ← green (security)
  X-Frame-Options           deny                        ← green (security)
  X-Content-Type-Options    nosniff                     ← green (security)
  Content-Security-Policy   default-src 'none'; ...     ← green (security)
  Referrer-Policy           no-referrer                 ← green (security)
  X-XSS-Protection          0

  ── Security Header Audit ──
  ✔  strict-transport-security
  ✔  x-frame-options
  ✔  x-content-type-options
  ✔  content-security-policy
  ✔  referrer-policy
  ⚠  MISSING: permissions-policy
  ⚠  MISSING: x-xss-protection
```

**Audited security headers:**

| Header | Purpose |
|--------|---------|
| `Strict-Transport-Security` | Forces HTTPS |
| `X-Frame-Options` | Clickjacking protection |
| `X-Content-Type-Options` | MIME sniffing prevention |
| `X-XSS-Protection` | Reflected XSS filter |
| `Content-Security-Policy` | Script/resource injection control |
| `Referrer-Policy` | Controls referrer leakage |
| `Permissions-Policy` | Feature/API access control |

---

### 09 — SSL Checker

**What it does:** Performs a TLS handshake with the target, reads the X.509 certificate, and reports: subject, issuer, SANs, validity window, days remaining, TLS version, and cipher suite. Warns on expired or soon-to-expire certs and deprecated TLS versions.

**Prompts:**
```
  [Enter domain (e.g. example.com)] ▶
  [Port (default 443)]               ▶
```

**Example — valid cert:**
```
  [Enter domain] ▶ github.com
  [Port]         ▶ 443
```

**Expected output:**
```
  ──────────────────────────────────────────────────
    ◆ SSL Checker
    Inspect TLS certificate details and expiry
  ──────────────────────────────────────────────────

  ℹ  Connecting to github.com:443 …

  Common Name           github.com
  Organization          GitHub, Inc.
  Issuer CN             DigiCert TLS Hybrid ECC SHA384 2020 CA1
  Issuer Org            DigiCert Inc
  SANs                  github.com, www.github.com
  Valid From            2024-03-07
  Valid Until           2025-03-07
  ✔  Valid for 141 more days

  TLS Version           TLSv1.3
  Cipher Suite          TLS_AES_128_GCM_SHA256
  Key Bits              128
  ✔  TLSv1.3 — acceptable protocol version.
```

**Expected output — expiring soon (< 30 days):**
```
  ⚠  Expires in 18 days — renew soon!
```

**Expected output — expired:**
```
  ✘  EXPIRED 12 days ago!
```

**Expected output — old TLS version:**
```
  ⚠  TLSv1.1 is outdated and insecure.
```

---

### 10 — Subdomain Finder

**What it does:** Resolves 200 common subdomain prefixes against the target domain in parallel threads. Prints hits in real time as they resolve.

**Built-in wordlist includes:** www, mail, api, dev, staging, admin, shop, blog, static, cdn, vpn, git, ci, status, grafana, and 185 more.

**Prompts:**
```
  [Enter domain (e.g. example.com)] ▶
  [Threads (default 50)]             ▶
```

**Example:**
```
  [Enter domain] ▶ google.com
  [Threads]      ▶ 50
```

**Expected output:**
```
  ──────────────────────────────────────────────────
    ◆ Subdomain Finder
    DNS brute-force subdomain enumeration
  ──────────────────────────────────────────────────

  ℹ  Probing 200 subdomains on google.com …

  ✔ www.google.com                         142.250.195.68
  ✔ mail.google.com                        142.250.72.197
  ✔ api.google.com                         142.251.163.95
  ✔ docs.google.com                        142.250.195.78
  ✔ news.google.com                        142.250.72.206
  ✔ cloud.google.com                       142.250.195.95
  ✔ blog.google.com                        216.239.34.21

  ✔  Found 7 subdomain(s).
```

**Example — no results:**
```
  [Enter domain] ▶ thisdoesnotexist99999.xyz
  ⚠  No subdomains resolved.
```

---

### 11 — Username Search

**What it does:** Probes 20 platforms via threaded HTTP requests to check whether a username profile page exists. Results print in real time as threads complete.

**Platforms checked:**
GitHub · GitLab · Instagram · Reddit · Twitch · X/Twitter · YouTube · TikTok · Pinterest · Tumblr · Medium · Dev.to · Keybase · HackerNews · Replit · Pastebin · Linktree · Steam · Twitch Clips · Mastodon

**Prompts:**
```
  [Enter username] ▶
```

**Example — known username:**
```
  [Enter username] ▶ torvalds
```

**Expected output:**
```
  ──────────────────────────────────────────────────
    ◆ Username Search
    Probe username existence across 20+ platforms
  ──────────────────────────────────────────────────

  ℹ  Checking 'torvalds' across 20 platforms …

  ✔ GitHub                https://github.com/torvalds
  ✔ Dev.to                https://dev.to/torvalds
  ✔ Keybase               https://keybase.io/torvalds

  ✔  Found on 3 / 20 platforms.
  ⚠  Not found / unreachable: 17 platform(s).

  [List platforms NOT found? [y/N]] ▶ y

  ✘ GitLab
  ✘ Instagram
  ✘ Reddit
  ✘ Twitch
  ✘ X / Twitter
  ...
```

**Example — non-existent username:**
```
  [Enter username] ▶ xzqwerty99887766nonsense

  ✔  Found on 0 / 20 platforms.
```

---

### 12 — Directory Bruteforce

**What it does:** Sends threaded HTTP GET requests to a target URL with paths from a built-in wordlist. Reports any response that isn't 404 or 400 — color-coded by status code.

**Built-in wordlist covers:** Admin panels, config files (`.env`, `.git`, `wp-config.php`), backup archives, API endpoints, framework paths, log files, and security files (`robots.txt`, `security.txt`).

**Status code colors:**
- Green: `200 OK`
- Yellow: `301/302 Redirect`, `403 Forbidden`
- Cyan: Other non-404 codes

**Prompts:**
```
  [Enter base URL (e.g. https://example.com)]                    ▶
  [Include extensions? [1] None [2] .php .html .txt (default 1)] ▶
  [Threads (default 30)]                                          ▶
```

**Example:**
```
  [Enter base URL] ▶ https://example.com
  [Extensions]     ▶ 1
  [Threads]        ▶ 30
```

**Expected output:**
```
  ──────────────────────────────────────────────────
    ◆ Directory Bruteforce
    HTTP path discovery via wordlist
  ──────────────────────────────────────────────────

  ℹ  Probing 180 paths on https://example.com …

  STATUS  URL
  ────────────────────────────────────────────────────────────
  [200]   https://example.com/robots.txt
  [200]   https://example.com/sitemap.xml
  [403]   https://example.com/admin
  [301]   https://example.com/login
  [200]   https://example.com/.well-known/security.txt

  ✔  Discovered 5 path(s).

  ■ 200 OK   ■ 301/302 Redirect   ■ 403 Forbidden   ■ Other
```

**Example — with extensions (mode 2):**
```
  [Extensions] ▶ 2

  [200]   https://example.com/config.php
  [200]   https://example.com/backup.zip
  [403]   https://example.com/admin.html
```

---

## Test Cases

All test cases below use **public, authorized targets** intended for testing. Never scan targets you do not own or have explicit permission to test.

---

### TC-01 · IP Lookup — Valid Public IP

```
Input:    8.8.8.8
Expected: Country=United States, City=Mountain View, ISP=Google LLC
Pass if:  kv table printed with non-empty values for all 10 fields
```

### TC-02 · IP Lookup — Hostname Auto-Resolution

```
Input:    scanme.nmap.org
Expected: Resolves to 45.33.32.156, ISP=Linode
Pass if:  IP shown is 45.33.32.156, geo data populated
```

### TC-03 · IP Lookup — Invalid / Unresolvable Host

```
Input:    not-a-real-host-xyzabc.invalid
Expected: ✘  Could not resolve 'not-a-real-host-xyzabc.invalid'
Pass if:  Error shown, no crash, menu returns
```

### TC-04 · IP Lookup — Private IP (loopback)

```
Input:    127.0.0.1
Expected: ✘  (ip-api returns status=fail for private ranges)
Pass if:  Error message shown, no crash
```

---

### TC-05 · Port Scanner — Known Open Ports

```
Target:   scanme.nmap.org
Mode:     Top ports
Timeout:  1.0s
Expected: 22/tcp open SSH, 80/tcp open HTTP
Pass if:  Both ports appear in output
```

### TC-06 · Port Scanner — Unreachable Host

```
Target:   192.0.2.1   (RFC 5737 TEST-NET — guaranteed unreachable)
Mode:     Top ports
Timeout:  0.3s
Expected: ⚠  No open ports found.
Pass if:  Zero open ports, no crash, completes within ~60s
```

### TC-07 · Port Scanner — Custom Range Hits

```
Target:   scanme.nmap.org
Range:    79-81
Timeout:  1.0s
Expected: 80/tcp open HTTP
Pass if:  Exactly port 80 reported, ports 79 and 81 not listed
```

### TC-08 · Port Scanner — Invalid Range Input

```
Target:   scanme.nmap.org
Range:    abc-xyz
Expected: ✘  Invalid range.
Pass if:  Error shown, returns to menu, no crash
```

---

### TC-09 · DNS Lookup — All Records for google.com

```
Domain:   google.com
Type:     ALL
Expected: A section (142.250.x.x), MX section (smtp.google.com.),
          NS section (ns1-4.google.com.), TXT section (v=spf1...)
Pass if:  At least A, MX, NS sections populated
```

### TC-10 · DNS Lookup — Specific MX Record

```
Domain:   gmail.com
Type:     MX
Expected: ── MX ──  with gmail-smtp-in.l.google.com
Pass if:  MX section shown, other record types not shown
```

### TC-11 · DNS Lookup — Non-Existent Domain

```
Domain:   thisdoesnotexist99999abc.com
Type:     A
Expected: ⚠  No DNS records found for 'thisdoesnotexist99999abc.com'
Pass if:  Warning shown, no crash
```

---

### TC-12 · Ping Test — Fast, Reachable Host

```
Target:   1.1.1.1
Count:    4
Expected: 4 green ● lines, 0% packet loss, ✔ Host is up.
Pass if:  All 4 packets received, latency shown in green (< 50ms typical)
```

### TC-13 · Ping Test — Unreachable Host (RFC 5737)

```
Target:   192.0.2.1
Count:    2
Expected: 100% packet loss, ⚠ Host unreachable or packet loss detected.
Pass if:  Warning shown, no crash, returns to menu
```

### TC-14 · Ping Test — Invalid Count Input

```
Target:   1.1.1.1
Count:    abc
Expected: Falls back to default count of 4, runs normally
Pass if:  4 packets sent, no crash
```

---

### TC-15 · Header Grabber — HTTPS Site

```
URL:      https://example.com
Expected: HTTP 200, headers table printed, security audit section shown
Pass if:  Status code 200, at least 5 headers listed, audit section present
```

### TC-16 · Header Grabber — Auto-Prefix HTTP

```
URL:      github.com   (no scheme)
Expected: Tool prepends https://, fetches https://github.com
Pass if:  HTTP 200, GitHub headers shown
```

### TC-17 · Header Grabber — Bad Domain

```
URL:      https://thisdoesnotexist99999abc.invalid
Expected: ✘  Connection failed: ...
Pass if:  Error shown, no crash, returns to menu
```

---

### TC-18 · SSL Checker — Valid Certificate

```
Domain:   github.com
Port:     443
Expected: TLSv1.3, days_left > 0, ✔ Valid for N more days
Pass if:  Cert not expired, TLS version shown, cipher shown
```

### TC-19 · SSL Checker — Non-TLS Port

```
Domain:   example.com
Port:     80
Expected: ✘  Connection failed (no TLS on port 80)
Pass if:  Error message shown, no crash
```

### TC-20 · SSL Checker — Invalid Domain

```
Domain:   thisdoesnotexist99999.xyz
Port:     443
Expected: ✘  Connection failed: [Errno -2] Name or service not known
Pass if:  Error shown, returns to menu
```

---

### TC-21 · Username Search — Known Username

```
Username: torvalds
Expected: ✔ GitHub  https://github.com/torvalds  (at minimum)
          Found on ≥ 1 / 20 platforms
Pass if:  GitHub match shown, summary count accurate
```

### TC-22 · Username Search — Gibberish Username

```
Username: xzqwerty99887766nonsensexxx
Expected: Found on 0 / 20 platforms.
Pass if:  No false positives, clean summary
```

### TC-23 · Username Search — Empty Input

```
Username: (just press Enter)
Expected: ✘  No username provided.
Pass if:  Error shown, returns to menu, no crash
```

---

### TC-24 · Subdomain Finder — Active Domain

```
Domain:   google.com
Threads:  50
Expected: www.google.com, mail.google.com found at minimum
Pass if:  At least 2 subdomains resolved, IPs shown alongside
```

### TC-25 · Subdomain Finder — Non-Existent Domain

```
Domain:   thisdoesnotexist99999abc.com
Threads:  50
Expected: ⚠  No subdomains resolved.
Pass if:  Zero results, no crash, completes in < 30s
```

---

### TC-26 · Directory Bruteforce — robots.txt Discovery

```
URL:      https://google.com
Mode:     1 (no extensions)
Threads:  30
Expected: [200] https://google.com/robots.txt
Pass if:  robots.txt (status 200) appears in output
```

### TC-27 · Directory Bruteforce — With Extensions

```
URL:      https://testphp.vulnweb.com   (deliberately vulnerable test site)
Mode:     2 (with .php .html .txt)
Threads:  20
Expected: Multiple [200] responses with .php paths
Pass if:  Extension paths shown, status codes correct
```

### TC-28 · Directory Bruteforce — No Scheme Auto-Fix

```
URL:      example.com   (no https://)
Expected: Tool prepends https://, probes https://example.com/...
Pass if:  Scan runs, results shown, no crash
```

---

### TC-29 · System Info — Always Passes Locally

```
Input:    (none — select option 6)
Expected: All sections populated: OS, Network, Disk, CPU/Memory, Uptime
Pass if:  No fields show "—" for OS/Python/Hostname/Disk, no crash
```

### TC-30 · OSINT Search — Special Characters in Target

```
Target:   user@example.com
Expected: All 15 URLs generated with URL-encoded @ (%40)
Pass if:  URLs contain %40, no raw @ in query strings
```

### TC-31 · Menu — Invalid Input Handling

```
Input:    abc
Expected: ✘  Invalid choice — enter a number (1–13).
Pass if:  Error shown, menu re-displays, no crash

Input:    0
Expected: ✘  Choice out of range (1–13).

Input:    99
Expected: ✘  Choice out of range (1–13).
```

### TC-32 · Ctrl+C Interrupt Handling

```
Action:   Start a long-running scan (e.g. subdomain finder), press Ctrl+C
Expected: ⚠  Module interrupted. → returns to menu
Pass if:  No traceback, menu re-displays cleanly
```

---

## Adding a New Module

### Step 1 — Create the module file

```python
# modules/my_module.py

from core.base import BaseModule
from core.config import C
from utils.helpers import pause


class MyModule(BaseModule):
    NAME  = "My Module"           # Shown in section header
    COLOR = C.CYAN                # Pick any color from core/config.py
    DESC  = "One-line description" # Shown under section header

    def run(self) -> None:
        self.header()                                  # Prints colored banner

        target = self.prompt("Enter target", self.COLOR)
        if not target:
            self.err("No input provided.")
            pause()
            return

        # ---- your logic here ----

        self.ok("Success message")                     # ✔ green
        self.warn("Warning message")                   # ⚠ yellow
        self.err("Error message")                      # ✘ red
        self.info("Info message")                      # ℹ cyan
        self.kv("Key",  "Value",  self.COLOR)          # aligned key/value pair

        pause()                                        # waits for Enter
```

### Step 2 — Register in modules/\_\_init\_\_.py

```python
from modules.my_module import MyModule   # ← add import

ALL_MODULES = [
    IPLookup,
    DomainLookup,
    # ... existing modules ...
    DirBruteforce,
    MyModule,                            # ← add to end of list
]
```

### Step 3 — Add menu entry in utils/helpers.py

```python
MENU_ITEMS = [
    (1,  "IP Lookup"),
    # ...
    (12, "Directory Bruteforce"),
    (13, "My Module"),                   # ← add here
    (14, "Exit"),                        # ← bump exit number
]
```

### Step 4 — Add menu color in core/config.py

```python
MENU_COLORS = [
    C.CYAN,     # 1  IP Lookup
    # ...
    C.WHITE,    # 12 Directory Bruteforce
    C.TEAL,     # 13 My Module            ← add color
    C.DIM,      # 14 Exit                 ← move exit color
]
```

### Step 5 — Update EXIT_CHOICE in main.py

```python
EXIT_CHOICE = 14   # was 13
```

### BaseModule helper reference

| Method | Signature | Output |
|--------|-----------|--------|
| `header()` | `self.header()` | Colored section banner with NAME + DESC |
| `prompt()` | `self.prompt(label, color)` | Styled input, returns stripped string |
| `ok()` | `self.ok(msg)` | `✔  msg` in green |
| `warn()` | `self.warn(msg)` | `⚠  msg` in yellow |
| `err()` | `self.err(msg)` | `✘  msg` in red |
| `info()` | `self.info(msg)` | `ℹ  msg` in cyan |
| `kv()` | `self.kv(key, val, color)` | `key                  val` aligned pair |

### Available colors (core/config.py)

```python
C.RED     C.GREEN    C.YELLOW   C.BLUE
C.MAGENTA C.CYAN     C.WHITE    C.ORANGE
C.PINK    C.LIME     C.TEAL     C.PURPLE
C.DIM     C.BOLD
```

---

## Troubleshooting

### `whois: command not found`
Affects Module 02. Fix:
```bash
sudo apt install whois          # Debian/Ubuntu/Kali
sudo pacman -S whois            # Arch
sudo dnf install whois          # Fedora
```

### `dig: command not found`
Affects Module 04. Fix:
```bash
sudo apt install dnsutils       # Debian/Ubuntu/Kali
sudo pacman -S bind-tools       # Arch
sudo dnf install bind-utils     # Fedora
```

### Port scanner returns zero results on a live host
- Increase timeout: try `1.0` or `2.0` seconds
- Confirm the host is reachable first with Module 07 (Ping)
- Some hosts block ICMP but allow TCP — ping may fail while ports are open
- Firewalls may drop scan traffic silently; try from a different network

### SSL checker shows `Connection refused`
- Confirm the domain actually uses HTTPS
- Try port `8443` for alternate SSL endpoints
- Some hosts rate-limit or block non-browser TLS handshakes

### Username search returns many false negatives
- Instagram, TikTok, and YouTube may return 200 for non-existent users (anti-scraping)
- Increase per-connection timeout in `username_search.py`:
  ```python
  with urllib.request.urlopen(req, context=CTX, timeout=10)  # was 6
  ```
- Some platforms geo-block requests or require cookies

### Colors not showing in terminal
```bash
export TERM=xterm-256color
python3 main.py
```

### `ModuleNotFoundError: No module named 'core'`
You are running from the wrong directory. Fix:
```bash
cd recon-x          # must be in the project root
python3 main.py     # correct
```
**Not:**
```bash
python3 recon-x/main.py    # wrong — relative imports fail
```

### Subdomain finder or port scanner hangs
- The tools are threaded; Ctrl+C will interrupt cleanly and return to the menu
- If threads are stuck on DNS: your DNS resolver may be slow or rate-limiting. Reduce thread count to `10`

---

## Legal Notice

> **RECON-X is intended for authorized security testing and educational use only.**

- Only scan systems, domains, or IP addresses you **own** or have **explicit written permission** to test.
- Unauthorized port scanning, directory brute-forcing, or subdomain enumeration may violate:
  - Computer Fraud and Abuse Act (CFAA) — United States
  - Computer Misuse Act — United Kingdom
  - IT Act — India
  - Equivalent cybercrime laws in your jurisdiction
- The authors accept **no liability** for any misuse of this toolkit.
- Always obtain written authorization before testing any system.
- Use responsibly.

---

**Author:** 

*KS ADITHIYAN* CyberSecurity Student


**Contributors :**

*Buvaneswaran EB*   [Github](github.com/buvaneswaraneb)

---


*RECON-X v1.0.0 — Built with Python 3 stdlib · Zero pip deps · Linux*

