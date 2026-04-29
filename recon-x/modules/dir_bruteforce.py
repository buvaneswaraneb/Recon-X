# modules/dir_bruteforce.py — HTTP directory and file brute-forcer

import urllib.request
import urllib.error
import threading
import ssl
from core.base import BaseModule
from core.config import C
from utils.helpers import pause

# Common directories and files wordlist
WORDLIST = [
    # Admin panels
    "admin", "administrator", "admin/login", "admin/dashboard", "wp-admin",
    "cpanel", "phpmyadmin", "panel", "manager", "control", "backend",
    # Config / sensitive files
    ".env", ".git", ".git/config", ".htaccess", ".htpasswd",
    "config.php", "config.yml", "config.json", "settings.py",
    "wp-config.php", "database.yml", "secrets.yml",
    # Common paths
    "login", "logout", "register", "signup", "dashboard", "portal",
    "api", "api/v1", "api/v2", "graphql", "swagger", "swagger-ui.html",
    "docs", "documentation", "help", "support", "faq",
    # Backups
    "backup", "backups", "backup.zip", "backup.tar.gz", "db.sql",
    "site.zip", "www.zip", "dump.sql", "old", "archive",
    # Common files
    "robots.txt", "sitemap.xml", "crossdomain.xml", "security.txt",
    ".well-known/security.txt", "humans.txt", "readme.md", "README.md",
    "CHANGELOG.md", "INSTALL.md", "LICENSE", "Dockerfile",
    # Dev / debug
    "test", "dev", "development", "debug", "phpinfo.php", "info.php",
    "shell.php", "cmd.php", "upload", "uploads", "files", "temp", "tmp",
    # Logs
    "logs", "log", "error.log", "access.log", "debug.log",
    # Frameworks
    "vendor", "node_modules", "static", "assets", "media", "images",
    "css", "js", "fonts", "wp-content", "wp-includes",
    # Common APIs
    "health", "status", "ping", "metrics", "actuator", "actuator/env",
    "actuator/health", "server-status", "server-info",
]

EXTENSIONS = ["", ".php", ".html", ".txt", ".bak", ".old"]

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode    = ssl.CERT_NONE


class DirBruteforce(BaseModule):
    NAME  = "Directory Bruteforce"
    COLOR = C.WHITE
    DESC  = "HTTP path discovery via wordlist"

    def __init__(self):
        self._found: list[tuple[str, int]] = []
        self._lock = threading.Lock()
        self._base_url = ""

    def _probe(self, path: str) -> None:
        url = f"{self._base_url}/{path}"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"},
        )
        try:
            with urllib.request.urlopen(req, context=CTX, timeout=5) as resp:
                code = resp.status
        except urllib.error.HTTPError as e:
            code = e.code
        except Exception:
            return

        # Report anything that isn't 404 / 400
        if code not in (400, 404):
            color = C.OK if code == 200 else (C.WARN if code in (301, 302, 403) else C.INFO)
            with self._lock:
                self._found.append((url, code))
                print(f"  {color}[{code}]{C.RESET}  {url}")

    def run(self) -> None:
        self.header()
        target = self.prompt("Enter base URL (e.g. https://example.com)", self.COLOR)
        if not target:
            self.err("No URL provided."); pause(); return

        if not target.startswith(("http://", "https://")):
            target = "https://" + target
        self._base_url = target.rstrip("/")

        ext_raw = self.prompt(
            "Include extensions? [1] None  [2] .php .html .txt  (default 1)", self.COLOR
        ) or "1"
        exts = EXTENSIONS if ext_raw == "2" else [""]

        threads_raw = self.prompt("Threads (default 30)", self.COLOR) or "30"
        try:
            max_threads = max(1, min(int(threads_raw), 100))
        except ValueError:
            max_threads = 30

        # Build full path list
        paths: list[str] = []
        for word in WORDLIST:
            for ext in exts:
                if ext and "." in word.split("/")[-1]:
                    continue  # skip adding ext to files that already have one
                paths.append(f"{word}{ext}")

        self._found.clear()
        self.info(f"Probing {len(paths)} paths on {self._base_url} …\n")
        print(f"  {C.BOLD}{'STATUS':<8}{'URL'}{C.RESET}")
        print(f"  {'─'*60}")

        active: list[threading.Thread] = []
        for path in paths:
            t = threading.Thread(target=self._probe, args=(path,), daemon=True)
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
            self.ok(f"Discovered {len(self._found)} path(s).")
            # Legend
            print(f"\n  {C.OK}■{C.RESET} 200 OK   "
                  f"{C.WARN}■{C.RESET} 301/302 Redirect   "
                  f"{C.WARN}■{C.RESET} 403 Forbidden   "
                  f"{C.INFO}■{C.RESET} Other")
        else:
            self.warn("Nothing interesting found.")

        pause()
