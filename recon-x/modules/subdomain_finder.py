# modules/subdomain_finder.py — DNS brute-force subdomain enumeration

import socket
import threading
from core.base import BaseModule
from core.config import C
from utils.helpers import pause

# Common subdomain wordlist (compact, effective)
WORDLIST = [
    "www", "mail", "ftp", "smtp", "pop", "imap", "webmail", "cpanel",
    "admin", "administrator", "portal", "dashboard", "panel", "login",
    "api", "api2", "dev", "development", "staging", "stage", "test",
    "sandbox", "demo", "beta", "alpha", "lab", "labs",
    "shop", "store", "blog", "news", "forum", "help", "support", "docs",
    "wiki", "kb", "status", "monitor", "grafana", "kibana",
    "vpn", "remote", "ssh", "rdp", "gateway", "proxy", "cdn",
    "static", "assets", "media", "img", "images", "uploads",
    "db", "database", "mysql", "postgres", "redis", "mongo",
    "app", "apps", "web", "server", "host", "ns1", "ns2", "dns",
    "mx", "smtp2", "mail2", "secure", "ssl", "owa", "exchange",
    "cloud", "aws", "gcp", "azure", "k8s", "docker",
    "git", "gitlab", "github", "jenkins", "ci", "cd", "jira", "confluence",
    "m", "mobile", "wap", "old", "new", "v2", "v3",
]


class SubdomainFinder(BaseModule):
    NAME  = "Subdomain Finder"
    COLOR = C.PURPLE
    DESC  = "DNS brute-force subdomain enumeration"

    def __init__(self):
        self._found: list[tuple[str, str]] = []
        self._lock = threading.Lock()

    def _try_sub(self, subdomain: str, domain: str) -> None:
        fqdn = f"{subdomain}.{domain}"
        try:
            ip = socket.gethostbyname(fqdn)
            with self._lock:
                self._found.append((fqdn, ip))
                print(f"  {self.COLOR}✔ {C.BOLD}{fqdn:<45}{C.RESET}  {ip}")
        except socket.gaierror:
            pass

    def run(self) -> None:
        self.header()
        domain = self.prompt("Enter domain (e.g. example.com)", self.COLOR)
        if not domain:
            self.err("No domain provided."); pause(); return

        threads_raw = self.prompt("Threads (default 50)", self.COLOR) or "50"
        try:
            max_threads = max(1, min(int(threads_raw), 200))
        except ValueError:
            max_threads = 50

        self._found.clear()
        self.info(f"Probing {len(WORDLIST)} subdomains on {domain} …\n")

        active: list[threading.Thread] = []
        for word in WORDLIST:
            t = threading.Thread(target=self._try_sub, args=(word, domain), daemon=True)
            active.append(t)
            t.start()
            if len(active) >= max_threads:
                for t in active:
                    t.join()
                active.clear()
        for t in active:
            t.join()

        print()
        if self._found:
            self.ok(f"Found {len(self._found)} subdomain(s).")
        else:
            self.warn("No subdomains resolved.")

        pause()
