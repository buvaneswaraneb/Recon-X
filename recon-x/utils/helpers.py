# utils/helpers.py — Shared utility functions

import os
import sys
import socket
import subprocess
from core.config import C, TOOL_NAME, TOOL_VERSION, TOOL_AUTHOR, MENU_COLORS


# ── Terminal ─────────────────────────────────────────────────────────────────

def clear() -> None:
    os.system("clear")


def pause() -> None:
    input(f"\n  {C.DIM}Press Enter to return to menu…{C.RESET}")


# ── Banner ────────────────────────────────────────────────────────────────────

BANNER = r"""
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗      ██╗  ██╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║      ╚██╗██╔╝
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║█████╗ ╚███╔╝ 
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║╚════╝ ██╔██╗ 
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║      ██╔╝ ██╗
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝      ╚═╝  ╚═╝
"""

def print_banner() -> None:
    clear()
    print(C.CYAN + C.BOLD + BANNER + C.RESET)
    print(f"  {C.DIM}v{TOOL_VERSION}  |  Modular Cybersecurity Recon Toolkit  |  Linux{C.RESET}")
    print(f"  {C.DIM}{TOOL_AUTHOR}{C.RESET}\n")


# ── Menu ──────────────────────────────────────────────────────────────────────

MENU_ITEMS = [
    (1,  "IP Lookup"),
    (2,  "Domain Lookup"),
    (3,  "Port Scanner"),
    (4,  "DNS Lookup"),
    (5,  "OSINT Search"),
    (6,  "System Info"),
    (7,  "Ping Test"),
    (8,  "Header Grabber"),
    (9,  "SSL Checker"),
    (10, "Subdomain Finder"),
    (11, "Username Search"),
    (12, "Directory Bruteforce"),
    (13, "Exit"),
]

def print_menu() -> None:
    print(f"  {C.BOLD}{'─'*46}{C.RESET}")
    for idx, (num, label) in enumerate(MENU_ITEMS):
        color = MENU_COLORS[idx]
        num_str = f"{num:>2}"
        print(f"  {color}{C.BOLD}[{num_str}]{C.RESET}  {color}{label}{C.RESET}")
    print(f"  {C.BOLD}{'─'*46}{C.RESET}\n")


# ── Network helpers ───────────────────────────────────────────────────────────

def resolve_host(host: str) -> str | None:
    """Return IPv4 for a hostname, or None on failure."""
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        return None


def is_valid_ip(ip: str) -> bool:
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


def run_cmd(cmd: list[str], timeout: int = 10) -> tuple[int, str, str]:
    """Run a subprocess and return (returncode, stdout, stderr)."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except FileNotFoundError:
        return -1, "", f"Command not found: {cmd[0]}"
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
