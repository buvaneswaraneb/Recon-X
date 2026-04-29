# modules/ssl_checker.py — TLS/SSL certificate inspector

import ssl
import socket
import datetime
from core.base import BaseModule
from core.config import C
from utils.helpers import pause


class SSLChecker(BaseModule):
    NAME  = "SSL Checker"
    COLOR = C.LIME
    DESC  = "Inspect TLS certificate details and expiry"

    def run(self) -> None:
        self.header()
        host = self.prompt("Enter domain (e.g. example.com)", self.COLOR)
        if not host:
            self.err("No host provided."); pause(); return

        host = host.replace("https://", "").replace("http://", "").split("/")[0]

        port_raw = self.prompt("Port (default 443)", self.COLOR) or "443"
        try:
            port = int(port_raw)
        except ValueError:
            port = 443

        self.info(f"Connecting to {host}:{port} …")

        ctx = ssl.create_default_context()
        try:
            with socket.create_connection((host, port), timeout=8) as sock:
                with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    version = ssock.version()
        except ssl.SSLCertVerificationError as e:
            self.warn(f"Certificate verification failed: {e}")
            # Try without verification to still show cert info
            ctx2 = ssl.create_default_context()
            ctx2.check_hostname = False
            ctx2.verify_mode = ssl.CERT_NONE
            try:
                with socket.create_connection((host, port), timeout=8) as sock:
                    with ctx2.wrap_socket(sock, server_hostname=host) as ssock:
                        cert = ssock.getpeercert()
                        cipher = ssock.cipher()
                        version = ssock.version()
            except Exception as e2:
                self.err(f"Connection failed: {e2}"); pause(); return
        except Exception as e:
            self.err(f"Connection failed: {e}"); pause(); return

        print()

        # ── Certificate details ────────────────────────────────────────────
        subject = dict(x[0] for x in cert.get("subject", []))
        issuer  = dict(x[0] for x in cert.get("issuer",  []))

        self.kv("Common Name",       subject.get("commonName", "—"), self.COLOR)
        self.kv("Organization",      subject.get("organizationName", "—"), self.COLOR)
        self.kv("Issuer CN",         issuer.get("commonName", "—"), self.COLOR)
        self.kv("Issuer Org",        issuer.get("organizationName", "—"), self.COLOR)

        # SANs
        sans = cert.get("subjectAltName", [])
        if sans:
            san_str = ", ".join(v for _, v in sans[:6])
            if len(sans) > 6:
                san_str += f" (+{len(sans)-6} more)"
            self.kv("SANs", san_str, self.COLOR)

        # Expiry
        not_after_raw = cert.get("notAfter", "")
        not_before_raw = cert.get("notBefore", "")
        fmt = "%b %d %H:%M:%S %Y %Z"
        try:
            not_after  = datetime.datetime.strptime(not_after_raw, fmt)
            not_before = datetime.datetime.strptime(not_before_raw, fmt)
            now        = datetime.datetime.utcnow()
            days_left  = (not_after - now).days

            self.kv("Valid From",  not_before.strftime("%Y-%m-%d"), self.COLOR)
            self.kv("Valid Until", not_after.strftime("%Y-%m-%d"), self.COLOR)

            if days_left < 0:
                self.err(f"EXPIRED {abs(days_left)} days ago!")
            elif days_left < 30:
                self.warn(f"Expires in {days_left} days — renew soon!")
            else:
                self.ok(f"Valid for {days_left} more days")
        except Exception:
            self.kv("Not After", not_after_raw, self.COLOR)

        # TLS version / cipher
        print()
        self.kv("TLS Version", version or "—", self.COLOR)
        if cipher:
            self.kv("Cipher Suite",  cipher[0] or "—", self.COLOR)
            self.kv("Key Bits",      str(cipher[2] or "—"), self.COLOR)

        # Warn on old protocols
        if version in ("SSLv2", "SSLv3", "TLSv1", "TLSv1.1"):
            self.warn(f"{version} is outdated and insecure.")
        else:
            self.ok(f"{version} — acceptable protocol version.")

        pause()
