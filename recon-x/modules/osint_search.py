# modules/osint_search.py — Generate OSINT search URLs for a target

import urllib.parse
from core.base import BaseModule
from core.config import C
from utils.helpers import pause


class OSINTSearch(BaseModule):
    NAME  = "OSINT Search"
    COLOR = C.MAGENTA
    DESC  = "Generate Google, Shodan, and OSINT dork URLs for a target"

    # (Label, URL template with {q} placeholder)
    SOURCES = [
        ("Google — site",          "https://www.google.com/search?q=site:{q}"),
        ("Google — inurl",         "https://www.google.com/search?q=inurl:{q}"),
        ("Google — intitle",       "https://www.google.com/search?q=intitle:{q}"),
        ("Google — filetype:pdf",  "https://www.google.com/search?q={q}+filetype:pdf"),
        ("Bing",                   "https://www.bing.com/search?q={q}"),
        ("DuckDuckGo",             "https://duckduckgo.com/?q={q}"),
        ("Shodan",                 "https://www.shodan.io/search?query={q}"),
        ("Censys",                 "https://search.censys.io/search?resource=hosts&q={q}"),
        ("Hunter.io",              "https://hunter.io/domain-search/{q}"),
        ("Have I Been Pwned",      "https://haveibeenpwned.com/account/{q}"),
        ("VirusTotal",             "https://www.virustotal.com/gui/domain/{q}"),
        ("URLScan.io",             "https://urlscan.io/search/#domain:{q}"),
        ("Wayback Machine",        "https://web.archive.org/web/*/{q}"),
        ("GitHub Search",          "https://github.com/search?q={q}&type=code"),
        ("Pastebin Search",        "https://pastebin.com/search?q={q}"),
    ]

    def run(self) -> None:
        self.header()
        target = self.prompt("Enter domain, IP, email, or username", self.COLOR)
        if not target:
            self.err("No target provided."); pause(); return

        q = urllib.parse.quote(target, safe="")

        print(f"\n  {self.COLOR}{C.BOLD}OSINT URLs for: {C.RESET}{target}\n")
        for label, template in self.SOURCES:
            url = template.format(q=q)
            print(f"  {self.COLOR}►{C.RESET} {C.BOLD}{label:<30}{C.RESET}")
            print(f"    {C.DIM}{url}{C.RESET}\n")

        self.info("Copy URLs into your browser to investigate.")
        pause()
