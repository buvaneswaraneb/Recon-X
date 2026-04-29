# modules/dns_lookup.py — DNS record lookup via `dig` or socket fallback

from core.base import BaseModule
from core.config import C
from utils.helpers import pause, run_cmd

RECORD_TYPES = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA", "PTR"]


class DNSLookup(BaseModule):
    NAME  = "DNS Lookup"
    COLOR = C.BLUE
    DESC  = "Query DNS records for a domain"

    def _dig(self, domain: str, rtype: str) -> list[str]:
        """Use dig to get records; parse the ANSWER SECTION."""
        rc, out, _ = run_cmd(["dig", "+noall", "+answer", rtype, domain], timeout=8)
        if rc == -1 or not out.strip():
            return []
        results = []
        for line in out.splitlines():
            line = line.strip()
            if line and not line.startswith(";"):
                results.append(line)
        return results

    def run(self) -> None:
        self.header()
        domain = self.prompt("Enter domain or IP", self.COLOR)
        if not domain:
            self.err("No input provided."); pause(); return

        print(f"\n  {C.DIM}Record types: {', '.join(RECORD_TYPES)}{C.RESET}")
        rtype_raw = self.prompt("Record type (default ALL)", self.COLOR).upper() or "ALL"

        types = RECORD_TYPES if rtype_raw == "ALL" else [rtype_raw]

        found_any = False
        for rtype in types:
            records = self._dig(domain, rtype)
            if records:
                found_any = True
                print(f"\n  {self.COLOR}{C.BOLD}── {rtype} ──{C.RESET}")
                for r in records:
                    # Parse dig output: name TTL class type value
                    parts = r.split(None, 4)
                    value = parts[4] if len(parts) >= 5 else r
                    print(f"  {C.WHITE}  {value}{C.RESET}")

        if not found_any:
            self.warn(f"No DNS records found for '{domain}'")

        pause()
