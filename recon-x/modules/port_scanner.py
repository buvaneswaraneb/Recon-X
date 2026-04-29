# modules/port_scanner.py — Threaded TCP port scanner

import socket
import threading
from core.base import BaseModule
from core.config import C
from utils.helpers import pause, resolve_host, is_valid_ip

# Common service names for well-known ports
SERVICES = {
    21: "FTP",    22: "SSH",    23: "Telnet",  25: "SMTP",
    53: "DNS",    80: "HTTP",   110: "POP3",   143: "IMAP",
    443: "HTTPS", 445: "SMB",   3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 6379: "Redis", 8080: "HTTP-Alt", 8443: "HTTPS-Alt",
    27017: "MongoDB", 9200: "Elasticsearch",
}

TOP_PORTS = list(SERVICES.keys()) + list(range(1, 1025))
TOP_PORTS = sorted(set(TOP_PORTS))


class PortScanner(BaseModule):
    NAME  = "Port Scanner"
    COLOR = C.YELLOW
    DESC  = "Threaded TCP connect scanner"

    def __init__(self):
        self._open: list[tuple[int, str]] = []
        self._lock = threading.Lock()

    def _scan_port(self, ip: str, port: int, timeout: float) -> None:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                if s.connect_ex((ip, port)) == 0:
                    svc = SERVICES.get(port, "unknown")
                    with self._lock:
                        self._open.append((port, svc))
        except Exception:
            pass

    def run(self) -> None:
        self.header()
        target = self.prompt("Enter IP or hostname", self.COLOR)
        if not target:
            self.err("No target provided."); pause(); return

        ip = target if is_valid_ip(target) else resolve_host(target)
        if not ip:
            self.err(f"Cannot resolve '{target}'"); pause(); return

        mode = self.prompt("Scan  [1] Top ports  [2] Custom range  (default 1)", self.COLOR) or "1"

        if mode == "2":
            raw = self.prompt("Port range (e.g. 1-65535)", self.COLOR)
            try:
                start, end = map(int, raw.split("-"))
                ports = list(range(start, end + 1))
            except ValueError:
                self.err("Invalid range."); pause(); return
        else:
            ports = TOP_PORTS

        timeout_raw = self.prompt("Timeout per port in seconds (default 0.5)", self.COLOR) or "0.5"
        try:
            timeout = float(timeout_raw)
        except ValueError:
            timeout = 0.5

        self._open.clear()
        self.info(f"Scanning {ip} — {len(ports)} ports (timeout={timeout}s) …\n")

        threads = []
        for port in ports:
            t = threading.Thread(target=self._scan_port, args=(ip, port, timeout), daemon=True)
            threads.append(t)
            t.start()
            # Cap concurrency
            if len(threads) >= 200:
                for t in threads:
                    t.join()
                threads.clear()
        for t in threads:
            t.join()

        if not self._open:
            self.warn("No open ports found.")
        else:
            self._open.sort()
            print(f"  {self.COLOR}{C.BOLD}{'PORT':<8}{'STATE':<10}{'SERVICE'}{C.RESET}")
            print(f"  {'─'*36}")
            for port, svc in self._open:
                self.kv(f"{port}/tcp", f"{'open':<10}{svc}", self.COLOR)

        print(f"\n  {C.DIM}Scanned {len(ports)} ports · {len(self._open)} open{C.RESET}")
        pause()
