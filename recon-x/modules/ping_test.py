# modules/ping_test.py — ICMP ping with latency stats

import re
from core.base import BaseModule
from core.config import C
from utils.helpers import pause, run_cmd


class PingTest(BaseModule):
    NAME  = "Ping Test"
    COLOR = C.TEAL
    DESC  = "ICMP ping with latency statistics"

    def run(self) -> None:
        self.header()
        target = self.prompt("Enter IP or hostname", self.COLOR)
        if not target:
            self.err("No target provided."); pause(); return

        count_raw = self.prompt("Packet count (default 4)", self.COLOR) or "4"
        try:
            count = max(1, min(int(count_raw), 20))
        except ValueError:
            count = 4

        self.info(f"Pinging {target} × {count} …\n")
        rc, out, err = run_cmd(["ping", "-c", str(count), target], timeout=30)

        if rc == -1:
            self.err(err); pause(); return

        output = out or err
        if not output.strip():
            self.err("No output from ping."); pause(); return

        # Print per-packet lines
        for line in output.splitlines():
            if "bytes from" in line:
                # Extract time
                m = re.search(r"time=([\d.]+)", line)
                ms = m.group(1) if m else "?"
                ms_f = float(ms) if ms != "?" else 0
                color = C.OK if ms_f < 50 else (C.WARN if ms_f < 150 else C.ERR)
                print(f"  {color}● {line.strip()}{C.RESET}")
            elif "Request timeout" in line or "100% packet loss" in line:
                print(f"  {C.ERR}✘ {line.strip()}{C.RESET}")

        # Summary stats
        print()
        for line in output.splitlines():
            if "packets transmitted" in line:
                self.info(line.strip())
            elif "rtt min" in line or "round-trip" in line:
                self.info(line.strip())

        if rc != 0:
            self.warn("Host unreachable or packet loss detected.")
        else:
            self.ok("Host is up.")

        pause()
