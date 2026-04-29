# modules/ip_lookup.py — Geo-IP lookup via ip-api.com (free, no key needed)

import urllib.request
import json
from core.base import BaseModule
from core.config import C
from utils.helpers import pause, is_valid_ip, resolve_host


class IPLookup(BaseModule):
    NAME  = "IP Lookup"
    COLOR = C.CYAN
    DESC  = "Geo-locate any public IP address or hostname"

    API = "http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,zip,lat,lon,isp,org,as,query"

    def run(self) -> None:
        self.header()
        target = self.prompt("Enter IP or hostname", self.COLOR)
        if not target:
            self.err("No input provided.")
            pause(); return

        # Resolve hostname → IP if needed
        ip = target if is_valid_ip(target) else resolve_host(target)
        if not ip:
            self.err(f"Could not resolve '{target}'")
            pause(); return

        self.info(f"Querying {ip} …")
        try:
            url = self.API.format(ip=ip)
            with urllib.request.urlopen(url, timeout=8) as resp:
                data = json.loads(resp.read())
        except Exception as e:
            self.err(f"Request failed: {e}")
            pause(); return

        if data.get("status") != "success":
            self.err(data.get("message", "Unknown error"))
            pause(); return

        print()
        fields = [
            ("IP",          data.get("query",      "—")),
            ("Country",     data.get("country",    "—")),
            ("Region",      data.get("regionName", "—")),
            ("City",        data.get("city",       "—")),
            ("Zip",         data.get("zip",        "—")),
            ("Latitude",    str(data.get("lat",    "—"))),
            ("Longitude",   str(data.get("lon",    "—"))),
            ("ISP",         data.get("isp",        "—")),
            ("Org",         data.get("org",        "—")),
            ("AS",          data.get("as",         "—")),
        ]
        for k, v in fields:
            self.kv(k, v, self.COLOR)

        pause()
