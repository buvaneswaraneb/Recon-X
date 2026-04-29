# modules/header_grabber.py — HTTP/S response header inspector

import urllib.request
import urllib.error
import ssl
from core.base import BaseModule
from core.config import C
from utils.helpers import pause

# Headers that reveal interesting security posture
SECURITY_HEADERS = {
    "x-frame-options", "x-content-type-options", "x-xss-protection",
    "strict-transport-security", "content-security-policy",
    "referrer-policy", "permissions-policy",
}

INTERESTING = {
    "server", "x-powered-by", "via", "x-generator", "x-drupal-cache",
    "x-runtime", "x-aspnet-version",
}


class HeaderGrabber(BaseModule):
    NAME  = "Header Grabber"
    COLOR = C.PINK
    DESC  = "Inspect HTTP response headers and security posture"

    def run(self) -> None:
        self.header()
        url = self.prompt("Enter URL (e.g. https://example.com)", self.COLOR)
        if not url:
            self.err("No URL provided."); pause(); return

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        self.info(f"Fetching headers from {url} …")

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
                headers = dict(resp.headers)
                status  = resp.status
                final_url = resp.url
        except urllib.error.HTTPError as e:
            headers = dict(e.headers)
            status  = e.code
            final_url = url
        except Exception as e:
            self.err(f"Connection failed: {e}"); pause(); return

        sc = C.OK if status < 400 else (C.WARN if status < 500 else C.ERR)
        print(f"\n  {sc}HTTP {status}{C.RESET}  {C.DIM}{final_url}{C.RESET}\n")

        # ── All headers ────────────────────────────────────────────────────
        print(f"  {self.COLOR}{C.BOLD}── All Headers ──{C.RESET}")
        for k, v in sorted(headers.items()):
            kl = k.lower()
            if kl in SECURITY_HEADERS:
                self.kv(k, v, C.OK)
            elif kl in INTERESTING:
                self.kv(k, v, C.WARN)
            else:
                self.kv(k, v, C.DIM)

        # ── Security header audit ──────────────────────────────────────────
        print(f"\n  {self.COLOR}{C.BOLD}── Security Header Audit ──{C.RESET}")
        present = [h for h in SECURITY_HEADERS if h in {k.lower() for k in headers}]
        missing = [h for h in SECURITY_HEADERS if h not in {k.lower() for k in headers}]

        for h in present:
            self.ok(h)
        for h in missing:
            self.warn(f"MISSING: {h}")

        pause()
