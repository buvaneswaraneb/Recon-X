# modules/domain_lookup.py — WHOIS via system `whois` command

from core.base import BaseModule
from core.config import C
from utils.helpers import pause, run_cmd


class DomainLookup(BaseModule):
    NAME  = "Domain Lookup"
    COLOR = C.GREEN
    DESC  = "WHOIS information for a domain name"

    # Fields we want to highlight from raw whois output
    HIGHLIGHT = {
        "domain name", "registrar", "creation date", "updated date",
        "registry expiry date", "name server", "dnssec",
        "registrant organization", "registrant country",
    }

    def run(self) -> None:
        self.header()
        domain = self.prompt("Enter domain (e.g. example.com)", self.COLOR)
        if not domain:
            self.err("No domain provided.")
            pause(); return

        self.info(f"Running WHOIS for {domain} …")
        rc, stdout, stderr = run_cmd(["whois", domain], timeout=15)

        if rc == -1:
            self.err(stderr or "whois command unavailable. Install with: sudo apt install whois")
            pause(); return

        output = stdout or stderr
        if not output.strip():
            self.err("No WHOIS data returned.")
            pause(); return

        print()
        printed = 0
        for line in output.splitlines():
            if ":" not in line:
                continue
            key, _, val = line.partition(":")
            key_clean = key.strip().lower()
            val_clean  = val.strip()
            if not val_clean or val_clean.startswith("%"):
                continue
            if key_clean in self.HIGHLIGHT:
                self.kv(key.strip(), val_clean, self.COLOR)
                printed += 1

        if printed == 0:
            # Fall back to raw output (trimmed)
            for line in output.splitlines()[:40]:
                if line.strip() and not line.startswith("%"):
                    print(f"  {line}")

        pause()
