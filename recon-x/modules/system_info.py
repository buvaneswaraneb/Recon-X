# modules/system_info.py — Local system information

import platform
import socket
import os
import shutil
from core.base import BaseModule
from core.config import C
from utils.helpers import pause, run_cmd


class SystemInfo(BaseModule):
    NAME  = "System Info"
    COLOR = C.ORANGE
    DESC  = "Hardware, OS, network interfaces, and resource usage"

    def _section(self, title: str) -> None:
        print(f"\n  {self.COLOR}{C.BOLD}── {title} ──{C.RESET}")

    def run(self) -> None:
        self.header()

        # ── OS / Platform ──────────────────────────────────────────────────
        self._section("OS / Platform")
        self.kv("OS",          platform.system(), self.COLOR)
        self.kv("Release",     platform.release(), self.COLOR)
        self.kv("Version",     platform.version()[:60], self.COLOR)
        self.kv("Machine",     platform.machine(), self.COLOR)
        self.kv("Processor",   platform.processor() or "—", self.COLOR)
        self.kv("Python",      platform.python_version(), self.COLOR)
        self.kv("Hostname",    socket.gethostname(), self.COLOR)

        # ── Network ────────────────────────────────────────────────────────
        self._section("Network")
        try:
            local_ip = socket.gethostbyname(socket.gethostname())
        except Exception:
            local_ip = "—"
        self.kv("Local IP", local_ip, self.COLOR)

        rc, out, _ = run_cmd(["ip", "-4", "addr", "show"])
        if rc == 0:
            for line in out.splitlines():
                line = line.strip()
                if line.startswith("inet "):
                    parts = line.split()
                    ip_cidr = parts[1]
                    iface   = parts[-1] if len(parts) > 2 else "?"
                    self.kv(f"  {iface}", ip_cidr, self.COLOR)

        # ── Disk ───────────────────────────────────────────────────────────
        self._section("Disk Usage  ( / )")
        total, used, free = shutil.disk_usage("/")
        gb = 1024 ** 3
        self.kv("Total", f"{total/gb:.1f} GB", self.COLOR)
        self.kv("Used",  f"{used/gb:.1f} GB",  self.COLOR)
        self.kv("Free",  f"{free/gb:.1f} GB",  self.COLOR)

        # ── CPU / Memory ───────────────────────────────────────────────────
        self._section("CPU / Memory")
        cpu_count = os.cpu_count() or "—"
        self.kv("CPU Cores", str(cpu_count), self.COLOR)

        rc, out, _ = run_cmd(["free", "-h"])
        if rc == 0:
            lines = out.splitlines()
            if len(lines) >= 2:
                headers = lines[0].split()
                values  = lines[1].split()
                for h, v in zip(headers, values[1:], strict=False):
                    self.kv(f"Mem {h}", v, self.COLOR)

        # ── Uptime ─────────────────────────────────────────────────────────
        self._section("Uptime")
        rc, out, _ = run_cmd(["uptime", "-p"])
        if rc == 0:
            self.kv("Uptime", out.strip(), self.COLOR)

        pause()
